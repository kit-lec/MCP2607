from dotenv import load_dotenv
load_dotenv()

import os
import requests
from langchain_openai.chat_models.base import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from ddgs import DDGS  # Duck Duck Go Search 검색엔진

print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}')
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print(f'\t✅ALPHA_VANTAGE_API_KEY={alpha_vantage_api_key[:5]}...')

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.1)

# ANSI 코드 출력용
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

# ──────────────────────────────────────────────────────────────
# 회사 심볼
# ─────────────────────────────────────────────────────────────

def ddg_search(query, max_results=5):
    # DDGS().text() 는 {"title", "href", "body"} 딕셔너리 리스트를 반환한다.
    results = DDGS().text(query, max_results=max_results)
    return "\n\n".join(
        f"{result['title']}\n{result['body']}\n({result['href']})"
        for result in results
    )

# pydantic 모델로 매개변수 스키마 정의
class StockMarketSymbolSearchToolArgsSchema(BaseModel):
    query: str = Field(
        description="The query you will search for. Example query: Stock Market Symbol for Apple Company"
    )

class StockMarketSymbolSearchTool(BaseTool):
    name: Type[str] = "StockMarketSymbolSearchTool"   # 📌Tool 이름은 띄어쓰기 안됨!
    description: Type[str] = """
        Use this tool to find the stock market symbol for a company.
        It takes a query as an argument.
        """

    # tool 호출시 실행되는 함수
    def _run(self, query):
        print('🟧StockMarketSymbolSearchTool 호출] query=', f"{RED}{query}{RESET}")
        result = ddg_search(query)
        print(f"\n🟧StockMarketSymbolSearchTool 호출 결과\n{GREEN}{result}{RESET}")
        return result

# @tool 을 사용하여 더욱 간단하게 tool 정의 가능.
# StockMarketSymbolSearchTool 을 @tool 로 정의
from langchain.tools import tool

@tool(
        name_or_callable="StockMarketSymbolSearchTool",  # tool 이름
        description="""   
        Use this tool to find the stock market symbol for a company.
        It takes a query as an argument.    
        """,   # @tool 의 description 은 함수의 docstring 보다 우선시 됨.
        args_schema=StockMarketSymbolSearchToolArgsSchema,
)
def search_stock_symbol(query):
    """
    Use this tool to find the stock market symbol for a company.
    It takes a query as an argument.
    """
    # ↑ 함수의 docstring 이 tool의 description 역할을 한다!

    print('🟧 search_stock_symbol 호출] query=', f"{RED}{query}{RESET}")
    result = ddg_search(query)
    print(f"\n🟧 search_stock_symbol 호출 결과\n{GREEN}{result}{RESET}")
    return result

# ──────────────────────────────────────────────────────────────
# 회사 개요 tool
# ──────────────────────────────────────────────────────────────

class CompanySymbolArgsSchema(BaseModel):
    symbol: str = Field(description="Stock symbol of the company.Example: AAPL,TSLA")


class CompanyOverviewTool(BaseTool):
    name: Type[str] = "CompanyOverview"
    description: Type[str] = """
    Use this to get an overview of the financials of the company.
    You should enter a stock symbol.
    """ 

    args_schema: Type[CompanySymbolArgsSchema] = CompanySymbolArgsSchema

    def _run(self, symbol):
        print('🟪CompanyOverviewTool 호출 symbol=', f"{RED}{symbol}{RESET}")

        # AlphaVantage 사용
        r = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}")
        result = r.json()        

        print(f"\n🟪CompanyOverviewTool 호출 결과\n{GREEN}{result}{RESET}")
        return result





agent = create_agent(
    model=llm,
    tools=[
        # StockMarketSymbolSearchTool(),    # <- 이 툴은 회사의 주식 심볼을 알아내는데 사용
        search_stock_symbol,    # @tool 로 정의한 함수는 Tool 객체로 변환됨!

        CompanyOverviewTool(),
    ],
)

prompt = """
    Give me financial information on Cloudflare's stock.
"""

if __name__ == "__main__":
    # print(f"좋아하는 색은 {RED}빨강색{RESET} {BLUE}파랑색{RESET} {YELLOW}노랑색{RESET} {GREEN}초록색{RESET} 임다")

    # print(ddg_search("엔비디아 의 stock symbol 을 알려줘"))

    result = agent.invoke({
        "messages": [{"role": "user", "content": prompt}],
    })

    print('📌', result['messages'][-1].content)
