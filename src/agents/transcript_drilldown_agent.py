import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.transcript_drilldown_tools import drilldown_transcript

_SYSTEM_PROMPT = (
    "You are a transcript analyst for post-call intelligence. "
    "Call the drilldown_transcript tool with the full query and transcript turns. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_transcript_drilldown_agent(query_and_transcript: str) -> dict:
    """ReAct agent: delegates to drilldown_transcript tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [drilldown_transcript])

    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=query_and_transcript)]},
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
