import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.knowledge_gap_tools import detect_knowledge_gaps

_SYSTEM_PROMPT = (
    "You are a knowledge gap detection agent. "
    "Call the detect_knowledge_gaps tool with the full input text. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_knowledge_gap_agent(text: str) -> dict:
    """ReAct agent: delegates to detect_knowledge_gaps tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [detect_knowledge_gaps])

    # "Agent (streaming): " is printed here; the detect_knowledge_gaps tool streams
    # its LLM tokens inline, so the user sees output as it arrives.
    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=text)]},
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
