from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from models import load_vectors_and_query
from generator import vector_embedding

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://9d01-189-204-144-186.ngrok-free.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clase para la estructura de la solicitud
class QueryRequest(BaseModel):
    query: str

# Definir el endpoint para realizar consultas
@app.post("/query")
async def query_model(request: QueryRequest):
    try:
        response = load_vectors_and_query(request.query)
        return {"answer": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para generar los vectores FAISS
@app.post("/generate")
async def generate_vectors():
    try:
        vector_embedding()
        return {"message": "Vectores generados exitosamente."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para subir archivos PDF
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_location = f"./pdf/{file.filename}"
        
        # Guardar el archivo subido
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        return {"info": f"Archivo {file.filename} guardado exitosamente."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Iniciar el servidor con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
