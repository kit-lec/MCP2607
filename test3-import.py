# 확인용
# 제대로 import 여부 + version 체크
import sys
print(sys.version)

# ✅ pip install streamlit
import streamlit as st 
print('streamlit', st.__version__)

# ✅ pip install langchain
import langchain
print('langchain', langchain.__version__)


import langchain_core
print('langchain_core', langchain_core.__version__)

from langchain.messages import HumanMessage, SystemMessage, AIMessage, AIMessageChunk
from langchain_core.messages.human import HumanMessage, HumanMessageChunk
from langchain_core.messages.system import SystemMessage, SystemMessageChunk
from langchain_core.messages.ai import AIMessage, AIMessageChunk

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.prompts.chat import ChatMessagePromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate

from langchain_core.example_selectors.length_based import LengthBasedExampleSelector
from langchain_core.example_selectors.base import BaseExampleSelector

from langchain_core.prompts.loading import load_prompt

from langchain_core.globals import set_llm_cache
from langchain_core.globals import set_debug

from langchain_core.caches import InMemoryCache

from langchain_core.documents import Document

from langchain_core.runnables.base import Runnable
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.runnables.base import RunnableLambda

from langchain_core.tools.base import BaseTool
from langchain_core.tools.simple import Tool
from langchain_core.tools.structured import StructuredTool

# ✅ pip install langchain-community
# ⏳langchain_community 2026년 5월 종료가 발표되어 더 이상 업데이트되지 않습니다. 
# 당장은 동작하지만 import할 때 경고가 출력.
import langchain_community
print("langchain_community", langchain_community.__version__)

from langchain_community.cache import SQLiteCache
from langchain_community.llms.loading import load_llm
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_loaders.sitemap import SitemapLoader  # USER_AGENT environment variable not set, consider setting it to identify your requests.
from langchain_community.document_loaders.csv_loader import CSVLoader

from langchain_community.document_transformers.html2text import Html2TextTransformer

from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
# ✅ pip install chromadb
import chromadb
print('chromadb', chromadb.__version__)

# ✅ pip install faiss-cpu
import faiss
print('faiss', faiss.__version__)


from langchain_community.retrievers.wikipedia import WikipediaRetriever

from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.sql_database import SQLDatabase

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# ✅ pip install langchain-unstructured
import langchain_unstructured
print("langchain_unstructured", langchain_unstructured.__version__)
from langchain_unstructured import UnstructuredLoader
# pdf , docx 파일 load 하려면 아래 설치.
# ✅ pip install unstructured  "unstructured[pdf]" "unstructured[docx]"  <-- torch 설치 하게 된다. 시간 많이 걸림

# ✅ pip install langchain-openai
import langchain_openai
print('langchain_openai', langchain_openai.__all__)
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_openai.llms.base import OpenAI
from langchain_openai.embeddings.base import OpenAIEmbeddings

from langchain_community.memory.kg import ConversationKGMemory

from langchain_classic.chains import LLMChain
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore

from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_text_splitters.character import CharacterTextSplitter

# ✅ pip install langchain_huggingface
import langchain_huggingface
print('langchain_huggingface', langchain_huggingface.__all__)
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import HuggingFacePipeline

import tiktoken
print('tiktoken', tiktoken.__version__)

# ✅ pip install langchain_ollama
import langchain_ollama
print('langchain_ollama', langchain_ollama.__version__)
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings


# https://docs.langchain.com/oss/python/releases/langchain-v1#create-agent
from langchain.agents import create_agent


from langchain_core.tools.simple import Tool
from langchain_core.tools.base import BaseTool

# 12
# from pydantic import BaseModel
import pydantic
print('pydantic', pydantic.__version__)

# ✅ pip install fastapi
import fastapi
print('fastapi', fastapi.__version__)

# ✅ pip install langchain-pinecone
import pinecone
print('pinecone', pinecone.__version__)
from pinecone import Pinecone
from langchain_pinecone.vectorstores import PineconeVectorStore

# 랭그래프 langgraph
import langgraph
from langgraph.graph import StateGraph



