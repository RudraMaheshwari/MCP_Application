import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.report_generator_tools import generate_period_report

_SYSTEM_PROMPT = (
    "You are a post-call analytics report writer. "
    "Call the generate_period_report tool with the full aggregated data. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_report_generator_agent(aggregated_data: str) -> dict:
    """ReAct agent: delegates to generate_period_report tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [generate_period_report])

    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=aggregated_data)]},
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
