from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.gap_report_prompt import GAP_REPORT_SYSTEM_PROMPT


@tool
def generate_gap_report(gaps_data: str) -> str:
    """
    Generate a prioritised knowledge gap report for the Prep team.

    Accepts a JSON string containing knowledge gaps detected across multiple call sessions:
      - Each gap has: topic, canonical_question, frequency, suggested_action, sample_session_ids
      - Period covered (from / to dates)
      - Total sessions analysed

    Returns a JSON string with gaps grouped by topic and ranked by frequency, including:
      - critical_gaps list (frequency >= 5 or suggested_action = add_tool)
      - action_breakdown by type (add_to_knowledge, clarify_policy, add_tool, escalate_to_human_only)
      - overall_health signal (green / amber / red)
      - one-sentence summary of the most urgent gap cluster

    suggested_action values:
      - add_to_knowledge   : answer exists but missing from knowledge base
      - clarify_policy     : policy is ambiguous or agent couldn't apply it
      - add_tool           : no tool exists to answer this question
      - escalate_to_human_only : outside AI scope by design

    Example input:
      {
        "period": {"from": "2026-05-06", "to": "2026-05-12"},
        "total_sessions": 142,
        "gaps": [
          {
            "topic": "order status without order ID",
            "canonical_question": "Can you check my order without an order number?",
            "frequency": 12,
            "suggested_action": "clarify_policy",
            "sample_session_ids": ["session-041", "session-019"]
          }
        ]
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=GAP_REPORT_SYSTEM_PROMPT),
        HumanMessage(content=gaps_data),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
