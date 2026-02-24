import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# --- CONFIGURACIÓN ---
DOCS_DIRECTORY = "data" 
os.makedirs(DOCS_DIRECTORY, exist_ok=True)

def initialize_rag_system():
    print("[1/4] Cargando documentos...")
    documents = []
    for file in os.listdir(DOCS_DIRECTORY):
        file_path = os.path.join(DOCS_DIRECTORY, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
    
    if not documents:
        print("Error: No hay documentos en la carpeta 'data'. Añade archivos para empezar.")
        return None

    print("[2/4] Fragmentando texto (Chunking)...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    print("[3/4] Generando Embeddings y Base Vectorial...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Usamos FAISS en lugar de Chroma para evitar errores de Pydantic v1 en Python 3.14
    vector_db = FAISS.from_documents(texts, embeddings)

    print("[4/4] Sistema RAG Inicializado con éxito.")
    return vector_db

def ask_rag(vector_db, query):
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    except:
        print("\n[!] Nota: No se detectó API Key de OpenAI. Configúrala para obtener respuestas.")
        return "Error de conexión con el LLM."

    # --- IMPLEMENTACIÓN MANUAL DE RAG (LCEL) PARA EVITAR ERRORES DE COMPATIBILIDAD ---
    # Esto evita usar 'langchain.chains' que está dando problemas en Python 3.14
    
    template = """Responde a la pregunta basándote únicamente en el contexto proporcionado:
    
    Contexto:
    {context}
    
    Pregunta: {question}
    
    Respuesta útil:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Creamos la cadena usando el lenguaje de expresión de LangChain (LCEL)
    rag_chain = (
        {"context": vector_db.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        response = rag_chain.invoke(query)
        return response
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

if __name__ == "__main__":
    if not os.listdir(DOCS_DIRECTORY):
        with open(os.path.join(DOCS_DIRECTORY, "ejemplo.txt"), "w", encoding="utf-8") as f:
            f.write("El sistema RAG fue implementado con éxito en Python 3.14 usando patrones LCEL.")
    
    rag_memory = initialize_rag_system()
    
    if rag_memory:
        print("\n--- SISTEMA LISTO ---")
        while True:
            pregunta = input("\nPregunta al RAG (o escibe 'salir'): ")
            if pregunta.lower() == 'salir': break
            
            respuesta = ask_rag(rag_memory, pregunta)
            print(f"\nRespuesta de la IA:\n{respuesta}")
