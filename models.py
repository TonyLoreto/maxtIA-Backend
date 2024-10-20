from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  # Importa el modelo de embeddings
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar el modelo de Ollama
# llm = ChatOllama(base_url="http://localhost:11434", model="llama3.2:1b")
llm = ChatOllama(base_url="http://localhost:11434", model="llama3.1")

# Definir el prompt
prompt = ChatPromptTemplate.from_template(
  """
    Carefully and deeply think to answer the following questions about the text:
    <context>
    {context}
    <context>
    Questions: {input}
  """
)

# Función para cargar el índice FAISS y realizar consultas
def load_vectors_and_query(query):
    # Inicializar el mismo modelo de embeddings usado para crear el índice
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Cargar el índice FAISS previamente guardado, pasando el modelo de embeddings
    vectors = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Crear la cadena de documentos y la cadena de recuperación
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Ejecutar la consulta
    response = retrieval_chain.invoke({'input': query})
    
    # Mostrar la respuesta
    print(response['answer'])

# Consulta de ejemplo
query = "Dame un resumen de 15 palabras del documento"
load_vectors_and_query(query)
