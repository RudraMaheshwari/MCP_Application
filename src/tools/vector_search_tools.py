from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.vector_search_prompt import VECTOR_SEARCH_SYSTEM_PROMPT


@tool
def semantic_search(query_and_documents: str) -> str:
    """
    Perform semantic similarity search over PostCallSummary key_facts.

    Accepts a JSON string containing:
      - query: the natural language search query
      - documents: list of PostCallSummary entries to search over, each with
                   session_id and key_facts array

    Returns a JSON string with:
      - matches: ranked list of sessions with relevance_score (0.0–1.0),
                 matched_key_facts, and explanation of why each matches
      - reformulations_used: alternate phrasings considered for broader recall
      - found: false if no documents scored >= 0.3

    Semantic search finds meaning-based matches, not keyword matches.
    "angry about delivery" will match "frustrated with shipping delay"
    even with no shared words.

    Example input:
      {
        "query": "customer angry about delivery",
        "documents": [
          {
            "session_id": "session-041",
            "key_facts": [
              "Customer called about order delivery delay",
              "Agent confirmed 3-day delay due to carrier issue"
            ]
          }
        ]
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=VECTOR_SEARCH_SYSTEM_PROMPT),
        HumanMessage(content=query_and_documents),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
