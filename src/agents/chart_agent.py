from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from src.model.llm import get_llm
from src.prompts.chart_prompt import CHART_SYSTEM_PROMPT
from src.tools.chart_tools import execute_chart_code


def build_agent():
    return create_agent(get_llm(), [execute_chart_code], prompt=CHART_SYSTEM_PROMPT)


def run_chart_agent(user_input: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
    return result["messages"][-1].content
