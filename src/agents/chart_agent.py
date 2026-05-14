from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.model.llm import get_llm
from src.prompts.chart_prompt import CHART_SYSTEM_PROMPT
from src.tools.chart_tools import execute_chart_code


def run_chart_agent(user_input: str) -> str:
    """ReAct agent: LLM writes matplotlib code, execute_chart_code tool runs it."""
    llm = get_llm()
    agent = create_react_agent(llm, [execute_chart_code])

    print("Agent (streaming): ", end="", flush=True)
    chart_result: str | None = None

    for chunk, _ in agent.stream(
        {"messages": [SystemMessage(content=CHART_SYSTEM_PROMPT), HumanMessage(content=user_input)]},
        stream_mode="messages",
    ):
        if isinstance(chunk, AIMessageChunk):
            for tc in getattr(chunk, "tool_call_chunks", []):
                args = tc.get("args", "")
                if args:
                    print(args, end="", flush=True)
        elif isinstance(chunk, ToolMessage):
            content = chunk.content
            chart_result = content if isinstance(content, str) else str(content)

    print()
    return chart_result or "ERROR: execute_chart_code tool did not return a result"
