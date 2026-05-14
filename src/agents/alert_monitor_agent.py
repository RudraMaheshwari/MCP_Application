import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.alert_monitor_tools import monitor_alerts

_SYSTEM_PROMPT = (
    "You are an alert detection system for a voice AI call centre. "
    "Call the monitor_alerts tool with the full summary and threshold data. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_alert_monitor_agent(summary_and_thresholds: str) -> dict:
    """ReAct agent: delegates to monitor_alerts tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [monitor_alerts])

    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=summary_and_thresholds)]},
        stream_mode="messages",
    ):
        if isinstance(chunk, ToolMessage):
            content = chunk.content
            tool_result = content if isinstance(content, str) else str(content)

    print()

    raw = (tool_result or "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Agent did not return valid JSON", "raw": raw}
