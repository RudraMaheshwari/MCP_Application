import re

from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.chart_prompt import CHART_SYSTEM_PROMPT
from src.utils.code_executor import run_code


def run_chart_agent(user_input: str) -> str:
    """Two-step: LLM writes code, executor runs it.

    Avoids the agent loop feeding the 300KB base64 result back to the LLM,
    which would exceed the context window.
    """
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content=CHART_SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ])

    code = str(response.content).strip()

    # Strip markdown fences if present
    match = re.search(r"```(?:python)?\n?(.*?)```", code, re.DOTALL)
    if match:
        code = match.group(1).strip()

    return run_code(code)
