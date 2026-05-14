import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.tools.cypher_query_tools import generate_cypher_query

_SYSTEM_PROMPT = (
    "You are a Neo4j Cypher query generator for a post-call knowledge graph. "
    "Call the generate_cypher_query tool with the full question and context. "
    "Return the tool output verbatim — do not modify or wrap the JSON."
)


def run_cypher_query_agent(question_and_context: str) -> dict:
    """ReAct agent: delegates to generate_cypher_query tool, returns parsed dict."""
    llm = get_llm()
    agent = create_react_agent(llm, [generate_cypher_query])

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
