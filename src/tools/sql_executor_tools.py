from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.sql_executor_prompt import SQL_EXECUTOR_SYSTEM_PROMPT


@tool
def execute_nl_to_sql(question_and_context: str) -> str:
    """
    Convert a natural language question into a parameterised SQL query for the post-call analytics database.

    Accepts a JSON string containing:
      - question: the natural language business question
      - deployment_id: the RBAC deployment scope (always injected into the WHERE clause)
      - context: optional extra context (e.g. date range, agent filter)

    Returns a JSON string with:
      - generated_sql: the parameterised SELECT query (no INSERT/UPDATE/DELETE)
      - parameters: list of $1, $2 ... values with their meanings
      - expected_columns: what columns the query returns
      - explanation: plain English description of what the query returns
      - answerable: false if the question cannot be answered from the schema

    Example input:
      {
        "question": "Which agents had the lowest QA scores last week?",
        "deployment_id": "dep-001",
        "context": "week of 2026-05-06"
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=SQL_EXECUTOR_SYSTEM_PROMPT),
        HumanMessage(content=question_and_context),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
