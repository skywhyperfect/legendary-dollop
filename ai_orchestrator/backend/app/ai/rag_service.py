import os
import glob
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Получаем путь к директории документов
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "rag", "documents")

vectorstore = None

def init_rag():
    """ Инициализация векторной базы RAG на старте приложения или по требованию """
    global vectorstore
    api_key = os.getenv("OPENAI_API_KEY", "mock")
    # Если ключ mock, пропускаем реальную инициализацию, чтобы не падал MVP без ключа
    if api_key == "mock" or api_key == "test_mock":
        print("Mock API Key detected. RAG initialization skipped (will use mock response).")
        return

    documents = []
    txt_files = glob.glob(os.path.join(DOCS_DIR, "*.txt"))
    for file_path in txt_files:
        loader = TextLoader(file_path, encoding='utf-8')
        documents.extend(loader.load())
    
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = FAISS.from_documents(texts, embeddings)
    print("RAG Vectorstore initialized successfully.")

def check_compliance(query: str) -> dict:
    """ Проверяет запрос (задачу/расписание) на соответствие приказам """
    api_key = os.getenv("OPENAI_API_KEY", "mock")
    
    if vectorstore is None or api_key == "mock" or api_key == "test_mock":
        # Возвращаем заглушку, если запускаем локально без OpenAI API
        return {
            "compliant": True,
            "query": query,
            "relevant_orders": ["ПРИКАЗ №76 (mock)"],
            "analysis": "Проверка пройдена успешно (Mock RAG)."
        }

    docs = vectorstore.similarity_search(query, k=2)
    context = "\n".join([d.page_content for d in docs])
    
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)
    prompt = f"""
    Исходя из следующих официальных приказов школы:
    {context}
    
    Оцени ситуацию/запрос: "{query}"
    Нарушает ли это приказы? Дай краткий анализ.
    """
    
    analysis = llm.predict(prompt)
    
    return {
        "compliant": "нарушает" not in analysis.lower() and "не допускается" not in analysis.lower(),
        "query": query,
        "relevant_orders": [d.metadata.get("source", "Unknown") for d in docs],
        "analysis": analysis
    }

def translate_to_checklist(order_text: str) -> list:
    """ Превращает сложный бюрократический текст в простой bullet-point список """
    api_key = os.getenv("OPENAI_API_KEY", "mock")
    if api_key == "mock" or api_key == "test_mock":
        return ["Первое важное правило (mock)", "Второе действие (mock)"]
        
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)
    prompt = f"""
    Переведи следующий бюрократический текст в простой, понятный пошаговый чек-лист для учителя.
    Выводи только пункты списка.
    
    Текст: {order_text}
    """
    
    result = llm.predict(prompt)
    return [line.strip("- *1234567890.") for line in result.split("\n") if line.strip()]
