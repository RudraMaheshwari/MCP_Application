from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.report_generator_prompt import REPORT_GENERATOR_SYSTEM_PROMPT


@tool
def generate_period_report(aggregated_data: str) -> str:
    """
    Generate a structured executive report from pre-aggregated call performance data.

    Accepts a JSON string containing aggregated metrics for a time period:
      - call_volume breakdown (total, complete, degraded, errored)
      - avg_qa_score and avg_sentiment_score
      - sentiment distribution across all calls
      - top issues by session count
      - compliance findings (which QA rules failed and how many times)
      - knowledge gaps ranked by frequency
      - write-back outcomes (CRM/Ticket adapter results)

    Returns a JSON string with all the above fields plus a narrative executive summary
    and a report_health signal (green / amber / red).

    Example input:
      {
        "period": {"from": "2026-05-06", "to": "2026-05-12"},
        "call_volume": {"total": 142, "complete": 138, "degraded": 3, "errored": 1},
        "avg_qa_score": 0.74,
        "avg_sentiment_score": -0.12,
        ...
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=REPORT_GENERATOR_SYSTEM_PROMPT),
        HumanMessage(content=aggregated_data),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
