from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.knowledge_extraction_prompt import KNOWLEDGE_EXTRACTION_SYSTEM_PROMPT


@tool
def extract_knowledge(text: str) -> str:
    """
    Extract structured knowledge from the given text.

    Analyses the text and returns a JSON object containing:
      - entities (people, orgs, products, concepts)
      - facts with confidence levels
      - key topics
      - action items with owners and due dates
      - relationships between entities
      - one-sentence summary

    Returns a JSON string on success, or an error message on failure.
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=KNOWLEDGE_EXTRACTION_SYSTEM_PROMPT),
        HumanMessage(content=text),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
