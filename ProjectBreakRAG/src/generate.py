from config import LLM_MODEL
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def obtener_llm():
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0
    )