import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.vector_search_tools import semantic_search

_SYSTEM_PROMPT = (
    "You are a semantic search engine for post-call summaries. "
    "Call the semantic_search tool with the full query and documents. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_vector_search_agent(query_and_documents: str) -> dict:
    """ReAct agent: delegates to semantic_search tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [semantic_search])

    print("Agent (streaming): ", end="", flush=True)
    tool_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=query_and_documents)]},
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
