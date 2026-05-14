from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.knowledge_gap_prompt import KNOWLEDGE_GAP_SYSTEM_PROMPT


@tool
def detect_knowledge_gaps(text: str) -> str:
    """
    Detect knowledge gaps, ambiguities, and missing information in the given text.

    Analyses the text and returns a JSON object containing:
      - unanswered questions with severity
      - missing information topics
      - ambiguous statements
      - incomplete topics with expansion suggestions
      - suggested follow-up questions
      - overall completeness score (0–100)
      - one-sentence gap summary

    Returns a JSON string on success, or an error message on failure.
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=KNOWLEDGE_GAP_SYSTEM_PROMPT),
        HumanMessage(content=text),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
