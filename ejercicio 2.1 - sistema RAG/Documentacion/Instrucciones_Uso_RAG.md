# MANUAL DE USUARIO: SISTEMA RAG v1.0

## 1. Introducción
Este manual describe el funcionamiento y uso del sistema **Retrieval-Augmented Generation (RAG)** desarrollado para el examen de informática. Este sistema permite que una Inteligencia Artificial responda preguntas basándose exclusivamente en documentos proporcionados por el usuario.

## 2. Requisitos Previos e Instalación
Antes de ejecutar la aplicación, es necesario preparar el entorno de Python.

### Instalación de Dependencias
Abre una terminal en la carpeta del proyecto y ejecuta el siguiente comando:
```bash
pip install -r requirements.txt
```
*Nota: Este comando instalará LangChain, ChromaDB y los modelos de procesamiento de lenguaje necesarios.*

## 3. Preparación de Datos (Carpeta 'data')
La "memoria" del sistema depende de los archivos que coloques en la carpeta `data/`.
- **Formatos admitidos**: Archivos `.pdf` y archivos de texto `.txt`.
- **Cómo añadir información**: Simplemente copia tus documentos (apuntes, manuales, normativas) dentro de la carpeta `data/` antes de iniciar el programa.
- **Recomendación**: Asegúrate de que los documentos tengan texto legible (no escaneos de imagen borrosos) para una mejor precisión.

## 4. Configuración de Inteligencia (Opcional)
El sistema utiliza modelos locales para buscar la información (gratuito), pero para redactar la respuesta final utiliza GPT (OpenAI).
- Para una experiencia completa, asegúrate de tener una `OPENAI_API_KEY` configurada en tu sistema.
- Si no dispones de una, el sistema te avisará, pero la lógica de búsqueda y análisis seguirá funcionando.

## 5. Ejecución del Sistema
Para poner en marcha el RAG, ejecuta el script principal:
```bash
python main_rag.py
```

### Proceso de Inicialización:
1. **[1/4] Carga**: El sistema busca y lee todos los archivos en `data/`.
2. **[2/4] Fragmentación**: Divide el texto para que la IA pueda digerirlo.
3. **[3/4] Indexación**: Crea la base de datos vectorial en la carpeta `vector_db/`.
4. **[4/4] Listo**: El sistema queda a la espera de tus preguntas.

## 6. Cómo interactuar con el Agente
Una vez inicializado, verás un cursor solicitando tu pregunta:
- **Preguntas Directas**: Haz preguntas específicas sobre el contenido de tus archivos (ej: "¿Qué dice el apartado 4 sobre la normativa?").
- **Contexto**: El agente solo responderá basándose en tus documentos. Si le preguntas algo que no está en los archivos, te dirá que no lo sabe (evitando inventar información).
- **Finalización**: Escribe `salir` para cerrar la aplicación de forma segura.

## 7. Mantenimiento
Si añades documentos nuevos a la carpeta `data/`, simplemente reinicia el programa para que el sistema los procese y los añada a su base de conocimiento.
