from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, GROQ_MODEL


llm = None

def get_llm():
    global llm
    if llm is None:
        llm = ChatGroq(model=GROQ_MODEL, groq_api_key=GROQ_API_KEY)
    return llm
