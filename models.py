from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar el modelo de Ollama
llm = ChatOllama(base_url="http://localhost:11434", model="llama3.1")

# Definir el prompt
prompt = ChatPromptTemplate.from_template(
  """
    Eres un asistente que busca ayudar a alunos y profesores de comunidades rurales en educación básica, que no tienen acceso
    a internet, si te llegan a saludar, regreasa el saludo de forma cortés, y por favor solo sobre temas STEM y los relacionados
    con desarrollo economico, cultural, educativo además de los pertinentes a los documentos cargados, no contestes preguntas sobre ocio:
    <context>
    {context}
    <context>
    Questions: {input}
  """
)

# Función para cargar el índice FAISS y realizar consultas
def load_vectors_and_query(query):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectors = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Crear la cadena de documentos y la cadena de recuperación
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # Ejecutar la consulta
    response = retrieval_chain.invoke({'input': query})
    
    return response['answer']
