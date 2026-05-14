import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.sql_executor_tools import execute_nl_to_sql

_SYSTEM_PROMPT = (
    "You are a SQL query generator for a post-call analytics database. "
    "Call the execute_nl_to_sql tool with the full question and context. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_sql_executor_agent(question_and_context: str) -> dict:
    """ReAct agent: delegates to execute_nl_to_sql tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [execute_nl_to_sql])

    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=question_and_context)]},
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
