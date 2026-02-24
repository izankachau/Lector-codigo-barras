import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI # Se puede sustituir por Ollama para 100% local

# --- CONFIGURACIÓN ---
DOCS_DIRECTORY = "data" # Carpeta donde pondrás tus PDFs o TXT
DB_DIRECTORY = "vector_db" # Donde se guardará la "memoria" del RAG
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

    print("[3/4] Generando Embeddings y Base Vectorial (Esto puede tardar la primera vez)...")
    # Usamos un modelo local gratuito de HuggingFace para no depender de API Keys
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vector_db = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )

    print("[4/4] Sistema RAG Inicializado con éxito.")
    return vector_db

def ask_rag(vector_db, query):
    # Aquí puedes configurar tu LLM. 
    # Si tienes una API KEY de OpenAI la usará, si no, puedes configurar Ollama local.
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    except:
        print("\n[!] Nota: No se detectó API Key de OpenAI. Para usar la generación, configúrala o usa Ollama.")
        return "Error de conexión con el LLM."

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever()
    )
    
    response = qa_chain.invoke(query)
    return response["result"]

if __name__ == "__main__":
    # Asegurémonos de tener documentos para probar
    if not os.listdir(DOCS_DIRECTORY):
        with open(os.path.join(DOCS_DIRECTORY, "ejemplo.txt"), "w", encoding="utf-8") as f:
            f.write("El sistema RAG (Retrieval-Augmented Generation) fue diseñado para que las IAs dejen de inventar cosas.")
            f.write("Fue implementado por primera vez en este examen de informática el 24 de febrero de 2026.")

    rag_memory = initialize_rag_system()
    
    if rag_memory:
        while True:
            pregunta = input("\nPregunta al RAG (o escibe 'salir'): ")
            if pregunta.lower() == 'salir': break
            
            respuesta = ask_rag(rag_memory, pregunta)
            print(f"\nRespuesta de la IA:\n{respuesta}")
