# MaxtIA

**MaxtIA** es una soluci梟 offline que, utilizando **RAGs** (Retrieval-Augmented Generation) y un servidor local, permite realizar consultas personalizadas de forma eficiente.

## Instalaci梟 de Ollama

Para utilizar MaxtIA, es necesario instalar Ollama localmente. Sigue estos pasos:

1. Selecciona el **CLI** adecuado seg煤n tu sistema operativo (SO).
2. Descarga la versi贸n deseada de Ollama. Para este proyecto, hemos optado por la versi贸n `ollama3.2` de 2B par谩metros.
3. Para m谩s informaci贸n detallada sobre la instalaci贸n de Ollama, visita el siguiente enlace:
   - [Instalaci贸n de Ollama](https://github.com/ollama/ollama?tab=readme-ov-file)

## Backend

El backend del proyecto est茅 compuesto por los siguientes 3 archivos principales:

### 1. `api.py`
Este archivo contiene los endpoints que permiten realizar las siguientes operaciones:

- **Cargar un archivo PDF**: Utilizando el endpoint `/upload`, puedes cargar archivos PDF para ser procesados.
- **Generar vectores y almacenarlos**: A trav茅s del endpoint `/generate`, puedes generar los vectores y almacenarlos localmente.
- **Realizar una consulta**: Utiliza el endpoint `/query` para hacer consultas a la IA con los datos cargados.

Este servicio corre en el puerto `8000` y se ejecuta utilizando el siguiente comando:

```bash
python api.py
