"""
[전체동작흐름]
sitemap.xml 요청
   └─ <sitemapindex>면 → 하위 sitemap들을 재귀적으로 다시 요청
   └─ <urlset>이면 → <url><loc> 목록 수집
         ↓
URL 필터링 (같은 도메인인지, 정규식 패턴에 맞는지)
         ↓
각 페이지 HTML 요청 → BeautifulSoup 파싱 → 텍스트 추출
         ↓
Document(page_content, metadata)로 하나씩 yield
"""

import re                                   # filter_urls 정규식 처리
from typing import Callable, Iterator, Optional
from urllib.parse import urlparse           # URL에서 도메인(netloc) 추출
import xml.etree.ElementTree as ET          # sitemap.xml 파싱 (표준 라이브러리)

import requests                             # HTTP 요청
from bs4 import BeautifulSoup               # HTML 파싱
from langchain_core.document_loaders import BaseLoader   # 로더 표준 인터페이스
from langchain_core.documents import Document            # LangChain 문서 객체
from tqdm import tqdm

# sitemap 표준 XML 네임스페이스
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# 꼭 짚어야 할 것은 NS입니다. 실제 sitemap.xml은 보통 이렇게 시작합니다
# <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
#   <url>
#     <loc>https://example.com/page1</loc>
#     <lastmod>2026-10-01</lastmod>
#   </url>
# </urlset>

def default_parsing_function(soup: BeautifulSoup) -> str:
    """기본 파싱 함수"""

    # 본문과 관계없는 태그를 HTML 에서 제거
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # 남은 텍스트를 줄바꿈으로 이어 붙이고, 앞뒤 공백 제거
    return soup.get_text(separator="\n", strip=True)


class SitemapLoader(BaseLoader):
    def __init__(
        self,
        web_path: str,                     # sitemap.xml 주소
        filter_urls: Optional[list[str]] = None,   # 허용할 URL 정규식 목록
        parsing_function: Optional[Callable[[BeautifulSoup], str]] = None,
        restrict_to_same_domain: bool = True,      # 다른 도메인 URL 차단
        max_depth: int = 10,               # sitemap index 재귀 최대 깊이
        continue_on_failure: bool = False, # 페이지 하나 실패 시 계속할지
        timeout: int = 15,                 # 요청 타임아웃(초)            
    ):
        self.web_path = web_path
        # 정규식은 미리 compile해 두면 URL마다 반복 매칭할 때 효율적
        self.filter_urls = [re.compile(p) for p in (filter_urls or [])]  # filter_urls or [] <- 기본값을 None으로 두고 내부에서 빈 리스트로 바꾸는 것은, 파이썬에서 가변 기본 인자(def f(x=[])) 함정을 피하는 관용 패턴
        # 사용자 함수가 없으면 기본 함수 사용
        self.parsing_function = parsing_function or default_parsing_function
        self.restrict_to_same_domain = restrict_to_same_domain
        self.max_depth = max_depth
        self.continue_on_failure = continue_on_failure
        
        # timeout 지정하지 않으면 requests는 응답이 올 때까지 무한정 기다립니다. 크롤러에서는 반드시 넣어야 합니다
        self.timeout = timeout     

        # "https://docs.python.org/sitemap.xml" → "docs.python.org"
        self.domain = urlparse(web_path).netloc   

        # Session: TCP 연결을 재사용해서 같은 서버에 여러 번 요청할 때 빠름
        # 페이지 수백 개를 같은 서버에서 받을 때, 매번 새로 연결하는 requests.get()보다 눈에 띄게 빠릅니다
        self.session = requests.Session()

        # 기본 User-Agent 가 없으면 요청 차단하는 사이트들 많음.
        self.session.headers["User-Agent"] = "Mozilla/5.0 (sitemap-loader)"


    # 큰 사이트는 sitemap을 하나로 두지 않고 계층으로 나눕니다
    # <!-- sitemap index: sitemap들의 목록 -->
    # <sitemapindex xmlns="...">
    #   <sitemap><loc>https://example.com/sitemap-blog.xml</loc></sitemap>
    #   <sitemap><loc>https://example.com/sitemap-docs.xml</loc></sitemap>
    # </sitemapindex>    
    # 그래서 <sitemap> 태그를 만나면 그 주소로 다시 _parse_sitemap을 호출하는 재귀 구조로 만들었습니다. 
    # 두 for 문 중 해당하는 쪽만 실행되므로, 같은 함수 하나로 두 형태를 모두 처리합니다
    def _parse_sitemap(self, url: str, depth: int = 0) -> list[dict]:
        """sitemap.xml 파싱"""

        # 재귀종료조건
        if depth > self.max_depth:
            return []

        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()   # 4xx / 5xx 면 예외 발생
        root = ET.fromstring(resp.content)

        entries = []

        # (1) sitemap index 인 경우: <sitemap><loc>하위 sitemap 주소</loc></sitemap>
        for sm in root.findall("sm:sitemap", NS):
            loc = sm.findtext("sm:loc", namespaces=NS)
            if loc:
                # 하쉬 sitemap 을 다시 파싱 (depth +1)
                entries.extend(self._parse_sitemap(loc.strip(), depth+1))

        # (2) 일반 sitemap 인 경우  <url><loc>페이지주소</loc></url>
        for u in root.findall("sm:url", NS):
            loc = u.findtext("sm:loc", namespaces=NS)
            if loc:
                entries.append({
                    "loc": loc.strip(),
                    "lastmod": u.findtext("sm:lastmod", namespaces=NS),  # sitemap 에 lastmod 정보가 없으면 None
                })

        return entries

    def _allowed(self, url: str) -> bool:
        """URL필터"""

        # 동일 도메인 제한.  sitemap 도메인과 다르면 거부
        if self.restrict_to_same_domain and urlparse(url).netloc != self.domain:
            return False

        # 정규식 필터
        if self.filter_urls and not any(p.match(url) for p in self.filter_urls):
            return False

        return True

    def lazy_load(self) -> Iterator[Document]:
        """문서 로딩"""

        # sitemap 전체에서 확보한 url  목록들
        entries = self._parse_sitemap(self.web_path)

        for entry in tqdm(entries, total=len(entries), desc="Loading sitemap", unit="page"):
            url = entry['loc']
            if not self._allowed(url):
                continue  # 필터에 걸리면 건너뜀

            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "lxml")

                yield Document(
                    page_content = self.parsing_function(soup),
                    metadata={
                        "source": url,
                        "loc": url,
                        "lastmod": entry['lastmod'],
                    }
                )

            except Exception:
                if not self.continue_on_failure:
                    raise  # 기본: 실패시 즉시 중단


if __name__ == "__main__":
    loader = SitemapLoader(
        web_path = "https://stability.ai/sitemap.xml",
        continue_on_failure=True,
    )
    docs = loader.load()   
    print(len(docs), docs[0].metadata)