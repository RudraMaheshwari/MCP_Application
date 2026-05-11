from langchain_openai import ChatOpenAI
from src.config.settings import OPENAI_API_KEY, MODEL_NAME


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=MODEL_NAME, api_key=OPENAI_API_KEY)
