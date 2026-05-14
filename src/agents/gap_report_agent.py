import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.gap_report_tools import generate_gap_report

_SYSTEM_PROMPT = (
    "You are a knowledge gap analyst for a voice AI deployment. "
    "Call the generate_gap_report tool with the full gap data. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_gap_report_agent(gaps_data: str) -> dict:
    """ReAct agent: delegates to generate_gap_report tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [generate_gap_report])

    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=gaps_data)]},
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
