from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

# Inicializar el modelo de Ollama
llm = ChatOllama(base_url="http://localhost:11434", model="llama3.2:1b")

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

# Clase para la estructura de la solicitud
class QueryRequest(BaseModel):
    query: str

# Cargar embeddings y FAISS index
def load_vectors():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectors = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
    return vectors

# Inicializar FAISS index y el retriever
vectors = load_vectors()

# Definir el endpoint para realizar consultas
@app.post("/query")
async def query_model(request: QueryRequest):
    try:
        # Crear la cadena de recuperación
        retriever = vectors.as_retriever()
        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # Ejecutar la consulta
        response = retrieval_chain.invoke({'input': request.query})

        # Devolver la respuesta generada
        return {"answer": response['answer']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Iniciar el servidor con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
