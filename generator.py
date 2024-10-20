from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Función para generar y guardar los embeddings y FAISS index
def vector_embedding():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Cargar documentos desde un directorio de PDF
    loader = PyPDFDirectoryLoader("./pdf")
    docs = loader.load()

    # Dividir los documentos en fragmentos para el procesamiento
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)

    # Crear el �ndice FAISS con los documentos y embeddings
    vectors = FAISS.from_documents(documents, embeddings)

    # Guardar el índice FAISS en un archivo local para consultas posteriores
    vectors.save_local("./faiss_index")
    print("Índice FAISS guardado exitosamente en './faiss_index'")
