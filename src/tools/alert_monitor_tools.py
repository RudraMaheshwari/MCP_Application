from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.alert_monitor_prompt import ALERT_MONITOR_SYSTEM_PROMPT


@tool
def monitor_alerts(summary_and_thresholds: str) -> str:
    """
    Evaluate a PostCallSummary against configured thresholds and determine which alerts to fire.

    Accepts a JSON string containing:
      - post_call_summary: the full PostCallSummary for one session
      - thresholds: the alert threshold configuration for this deployment

    Threshold fields:
      - min_qa_score        : fires qa_drop alert if qa_weighted_score falls below this
      - max_gaps_per_session: fires gap_surge alert if knowledge_gaps count exceeds this
      (compliance_finding and sentiment_spike are always checked — no threshold needed)

    Alert types:
      - qa_drop            : QA score below threshold
      - compliance_finding : any no_policy_breach QA rule returned fail
      - sentiment_spike    : overall sentiment is very_negative
      - gap_surge          : knowledge gaps count exceeds threshold

    Returns a JSON string with:
      - alerts_fired list (empty if none breached)
      - no_alerts_fired flag
      - call_health (green / amber / red)
      - one-sentence summary of the alert situation

    Example input:
      {
        "post_call_summary": {
          "session_id": "session-041",
          "qa_weighted_score": 0.45,
          "sentiment_overall_label": "very_negative",
          "sentiment_overall_score": -0.81,
          "call_health_final": "red",
          "qa": {
            "per_rule": [
              {"rule_id": "no_policy_breach", "outcome": "fail", "evidence": "Turn 12: ..."}
            ]
          },
          "knowledge_gaps": [{}, {}, {}, {}, {}, {}]
        },
        "thresholds": {
          "min_qa_score": 0.60,
          "max_gaps_per_session": 3
        }
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=ALERT_MONITOR_SYSTEM_PROMPT),
        HumanMessage(content=summary_and_thresholds),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
