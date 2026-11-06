import os
import time
import hashlib
import json
from  pathlib import Path

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # OPENAI_API_KEY 필요!
#─────────────────────────────────────────────────────────────────────────────────────────
import streamlit as st

from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.runnables.base import RunnableLambda
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_unstructured import UnstructuredLoader
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

# LangChain 의 context 안에 있는 callback handler 는
# 기본적으로 LLM 의 event 를 listen 하는 class 다. 가령.
# ex) LLM 이 무언가를 만들기 시작할때,  작업을 끝낼 때,  LLM 이 글자를 생성하거나,  
#     streaming 할때, LLM 에 에러가 발생할때.. 등등
# callback handler 를 사용하여 log 를 작성하거나 analytics 등으로 보내는 등의 유용한 동작을 구현해볼수 있다.
from langchain_core.callbacks.base import BaseCallbackHandler

# ────────────────────────────────────────
# 🎃 LLM 로직
# ────────────────────────────────────────

class ChatCallbackHandler(BaseCallbackHandler):
    # CallbackHandler 는 event 들을 listen 하는 여러 함수들이 있다.
    # on_xxx() 으로 시작하는 함수들을 오버라이딩 하여 구현한다
    #    ex) LLM 상에서 발생한 event 를 다루는 함수들
    #       chain, retriever, 혹은 agent 에 대한 함수들도 있다.
    #    이벤트핸들러 함수 참조: https://python.langchain.com/api_reference/core/callbacks/langchain_core.callbacks.base.BaseCallbackHandler.html#langchain_core.callbacks.base.BaseCallbackHandler

    # ↓ on_llm_start() : LLM 작업 시작할때 호출
    #   많은 argument 들이 있지만 이번예제에선 걍 *args, **kwargs 로 받아낸다.  
    def on_llm_start(self, *args, **kwargs):
        self.message = ""
        self.message_box = st.empty()  # token 텍스트들로 채워나갈 메세지 박스

    # ↓ on_llm_end() : LLM 작업 종료할때 호출
    def on_llm_end(self, *args, **kwargs):
        # LLM 의 답변이 끝나면, 메세지를 저장
        save_message(self.message, "ai")

    # ↓ on_llm_new_token() : LLM이 생성해내는 새로운 token 마다 호출
    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)  # 새로운 token 이 추가될때마다 추가된 message 로 업데이트.


llm = ChatOpenAI(
    model='gpt-4o',
    temperature=0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),
    ],
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Answer the question using ONLY the following context.
        If you don't know the answer just say you don't know. DON'T make anything up.            

        Context: {context}
    """),
    ("human", "{question}"),
])


def format_docs(docs):
    """retrieve 된 Document 들을 하나의 문자열로 만들기"""
    return "\n\n".join(doc.page_content for doc in docs)

def call_chain(retriever, message):
    chain = (
        {
            # ② chain 의 input 을 이용해 retriever 를 자동으로 invoke => 결과 List[Document]
            # ③ 위 결과를 우리가 원하는 포맷(str)으로 변환하는 함수(format_docs)의 입력으로 전달.
            #   함수의 리턴값 str 이 'context' 값에 저장
            "context": retriever | RunnableLambda(format_docs),
            # ④ chain 의 input 이 'question' 값에도 전달된다. 
            "question": RunnablePassthrough(),
        }
        | prompt 
        | llm
    )

    response = chain.invoke(message)
    return response

# ────────────────────────────────────────
# 🍇 file load & cache
# ────────────────────────────────────────
upload_dir = r'./.cache/files'
embedding_dir = r'./.cache/embeddins'
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)
if not os.path.exists(embedding_dir):
    os.makedirs(embedding_dir)

class FileCacheEmbeddings(Embeddings):
    """임베딩 결과를 파일로 캐싱하는 래퍼 (CacheBackedEmbeddings 대체)

    - 처음 보는 문장만 실제 모델(underlying)에 보내고,
      계산한 벡터는 파일로 저장해 두었다가 다음에는 파일에서 꺼내 쓴다.
    """

    def __init__(self, underlying: Embeddings, cache_dir: str, namespace: str = ""):
        self.underlying = underlying          # 실제 임베딩 모델 (캐시 미스일 때만 호출)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.namespace = namespace            # 모델 이름 → 모델별로 캐시 분리

    def _path(self, text: str) -> Path:
        # 문장 → SHA-256 해시 → 캐시 파일 경로
        raw = (self.namespace + text).encode("utf-8")
        key = hashlib.sha256(raw).hexdigest()
        return self.cache_dir / f"{key}.json"

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        results: list = [None] * len(texts)   # 입력 순서대로 결과 자리 확보
        missing = []                          # 캐시에 없는 문장의 인덱스

        for i, text in enumerate(texts):
            p = self._path(text)
            if p.exists():
                results[i] = json.loads(p.read_text())   # 캐시 히트
            else:
                missing.append(i)                        # 캐시 미스

        if missing:  # 없는 것만 모아서 한 번에 모델에 요청
            new_vectors = self.underlying.embed_documents([texts[i] for i in missing])
            for i, vec in zip(missing, new_vectors):
                self._path(texts[i]).write_text(json.dumps(vec))
                results[i] = vec

        return results

    def embed_query(self, text: str) -> list[float]:
        # 쿼리는 캐싱하지 않고 매번 모델에 요청
        return self.underlying.embed_query(text)


# ------------------------------------------------------------------------
# 사용자가 메세지를 보내거나 UI  에 새로운 데이터가 생길때 마다,
# Streamlit 은 *.py 파일을 위에서 아래 방향으로 실행한다.
# 그 말은 embed_file() 도 다시 호출된다는 말이다.  
# 파일이 변경되지 않았슴에도 이 모든 과정을 다시 또 한다는 것은 매우 비효율적이다. (시간! 비용!)

# @st.cache_resource
#   최초 embed_file(file) 호출시 실행될것이다.  그리고 리턴값을 cache 해둔다.
#   그러나 두번째 호출시에는 만약 이 매개변수 file 이 동일하다면  
#                          (즉 유저가 다른 파일을 올리지 않았다면)
#   Streamlit 은 이 함수의 호출을 재실행하지 않는다.
#   대신에! 기존에 리턴했던 cache 되었던 값을 다시 리턴된다!

@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    file_content = file.read()
    file_path = os.path.join(upload_dir, file.name)

    with open(file_path, "wb") as f:
        f.write(file_content)

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    # UnstructuredLoader 는 문서를 요소(제목, 문단 등) 단위의 여러 Document 로 읽어온다.
    loader = UnstructuredLoader(file_path)
    docs = loader.load()
    # 이를 하나의 Document 로 합친뒤 split 할거다
    merged = Document(
        page_content="\n\n".join(doc.page_content for doc in docs),
        metadata={"source": file_path},
    )
    docs = splitter.split_documents([merged])

    embeddings = OpenAIEmbeddings()
    cached_embeddings = FileCacheEmbeddings(
        embeddings,
        os.path.join(embedding_dir, file.name),  # 각 파일마다 별도의 임베딩 캐시 디렉토리에 저장.
        namespace=embeddings.model,   # 사용하는 모델 이름으로 캐시 분리.
    )

    vectorstore = FAISS.from_documents(docs, cached_embeddings)

    retriever = vectorstore.as_retriever()
    return retriever

# 챗봇 message 로직
def save_message(message, role):
    st.session_state['messages'].append({"message": message, "role": role})

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)  

def paint_history():
    for message in st.session_state['messages']:
        send_message(message['message'], message['role'], save=False)


# ────────────────────────────────────────
# ⭕ Streamlit 로직
# ────────────────────────────────────────
st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📃",
)

st.title("Document GPT")

with st.sidebar:
    file = st.file_uploader(
        label="Upload a .txt .pdf or .docs file",
        type=["pdf", "txt", "docx"],
    )

if file:
    retriever = embed_file(file)
    # docs = retriever.invoke("Where does Winston live?")
    # st.write(len(docs))
    # st.write(docs)

    send_message("준비되었습니다. 질문해보세요!", "ai", save=False)
    paint_history()
    message = st.chat_input("업로드한 file에 대해 질문을 남겨보세요...")
    if message:
        send_message(message, "human")

        with st.chat_message("ai"):
            response = call_chain(retriever, message)


        


        

else:
    st.markdown(
        """
    안녕하세요!

    이 챗봇을 사용해서 여러분의 파일들에 대해 AI에게 물어보세요!  

    sidebar 에 파일을 업로드 해두세요.
    """
    )

    st.session_state['messages'] = []    