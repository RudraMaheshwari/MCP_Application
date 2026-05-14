from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.transcript_drilldown_prompt import TRANSCRIPT_DRILLDOWN_SYSTEM_PROMPT


@tool
def drilldown_transcript(query_and_transcript: str) -> str:
    """
    Extract and summarise the most relevant turns from a call transcript for a given topic or question.

    Accepts a JSON string containing:
      - session_id: the session being inspected
      - query: the topic, question, or issue to search for in the transcript
      - turns: list of transcript turns, each with turn_index, speaker, and content

    Returns a JSON string with:
      - relevant_turns: the turns directly relevant to the query (with verbatim content)
      - context_turns: surrounding turns (2 before/after each relevant turn) for readability
      - summary: 2–3 sentence summary of what happened in the relevant section
      - sentiment_at_section: sentiment of the relevant section
      - found: false if the topic does not appear in the transcript

    Use this to drill into a specific session after a broader search has identified it,
    or to fetch the transcript context behind a citation in an insight answer.

    Example input:
      {
        "session_id": "session-041",
        "query": "order lookup failure",
        "turns": [
          { "turn_index": 0, "speaker": "customer", "content": "Hi, I need help with my order." },
          { "turn_index": 1, "speaker": "agent", "content": "Sure, can I get your order number?" },
          { "turn_index": 2, "speaker": "customer", "content": "I don't have it with me." },
          { "turn_index": 3, "speaker": "agent", "content": "I'm unable to look up orders without the order ID." }
        ]
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=TRANSCRIPT_DRILLDOWN_SYSTEM_PROMPT),
        HumanMessage(content=query_and_transcript),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
