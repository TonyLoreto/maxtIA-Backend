from langchain_community.chat_models import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os
# from IPython.display import display, Markdown

load_dotenv()

llm = ChatOllama(base_url="http://localhost:11434", model="llama3.2:1b")

prompt = ChatPromptTemplate.from_template(
  """
    Carefully and deeply think to answer the following questions about the text:
    <context>
    {context}
    <context>
    Questions: {input}
  """
)

def md(t):
    print(t)

def vector_embedding():
  embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
  loader = PyPDFDirectoryLoader("./pdf")
  print(loader)
  docs = loader.load()
  print(docs)
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  documents = text_splitter.split_documents(docs[:20])
  print(documents)
  vectors = FAISS.from_documents(documents, embeddings)
  return vectors

vectors = vector_embedding()

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vectors.as_retriever()

retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({'input': 'Dame un resumen de 15 palabras del documento'})

md(response['answer'])

