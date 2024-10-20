# MaxtIA

**MaxtIA** es una solución offline que, utilizando **RAGs** (Retrieval-Augmented Generation) y un servidor local, permite realizar consultas personalizadas de forma eficiente.

## Instalación de Ollama

Para utilizar MaxtIA, es necesario instalar Ollama localmente. Sigue estos pasos:

1. Selecciona el **CLI** adecuado según tu sistema operativo (SO).
2. Descarga la versión deseada de Ollama. Para este proyecto, hemos optado por la versión `ollama3.2` de 2B parámetros.
3. Para más información detallada sobre la instalación de Ollama, visita el siguiente enlace:
   - [Instalación de Ollama](https://github.com/ollama/ollama?tab=readme-ov-file)

## Backend

El backend del proyecto esté compuesto por los siguientes 3 archivos principales:

### 1. `api.py`
Este archivo contiene los endpoints que permiten realizar las siguientes operaciones:

- **Cargar un archivo PDF**: Utilizando el endpoint `/upload`, puedes cargar archivos PDF para ser procesados.
- **Generar vectores y almacenarlos**: A través del endpoint `/generate`, puedes generar los vectores y almacenarlos localmente.
- **Realizar una consulta**: Utiliza el endpoint `/query` para hacer consultas a la IA con los datos cargados.

Este servicio corre en el puerto `8000` y se ejecuta utilizando el siguiente comando:

```bash
python api.py
