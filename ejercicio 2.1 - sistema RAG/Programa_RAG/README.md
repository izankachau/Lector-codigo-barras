# Sistema RAG (Retrieval-Augmented Generation)

Este proyecto implementa un sistema de Generación Aumentada por Recuperación que permite consultar documentos locales (PDF y TXT) utilizando Inteligencia Artificial.

## Estructura
- `main_rag.py`: Script principal del sistema.
- `data/`: Carpeta donde debes colocar tus archivos PDF o TXT para que la IA los aprenda.
- `vector_db/`: Carpeta donde se guarda la base de datos vectorial (memoria).

## Instalación
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Coloca tus archivos en la carpeta `data/`.

3. Ejecuta el programa:
   ```bash
   python main_rag.py
   ```

## Notas
- El sistema utiliza `HuggingFaceEmbeddings` de forma local, por lo que la primera vez descargará el modelo (aprox. 100MB).
- Para la generación de respuestas, se recomienda configurar una `OPENAI_API_KEY` en el entorno, o modificar el script para usar un LLM local como Ollama.
