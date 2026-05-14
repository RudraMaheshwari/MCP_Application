from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from src.model.llm import get_llm
from src.prompts.cypher_query_prompt import CYPHER_QUERY_SYSTEM_PROMPT


@tool
def generate_cypher_query(question_and_context: str) -> str:
    """
    Convert a natural language question about graph relationships into a Neo4j Cypher query.

    Accepts a JSON string containing:
      - question: the natural language question about relationships in the knowledge graph
      - deployment_id: the RBAC deployment scope (injected into every query)
      - context: optional extra context (e.g. time window, specific topic)

    The knowledge graph contains:
      Nodes:  Session, Gap, Topic, Customer, Policy
      Edges:  REVEALED, BELONGS_TO, HAD, RAN_WITH, TRACES_TO

    Best suited for relationship and pattern questions such as:
      - "Which gap topics always appear together in the same session?"
      - "Which customers have hit the same knowledge gap 3 or more times?"
      - "Which gaps all trace back to the same policy?"
      - "How did a topic's frequency change after a Manifesto update?"

    Returns a JSON string with:
      - generated_cypher: the read-only MATCH ... RETURN query
      - parameters: $deployment_id and any other parameters
      - traversal_pattern: description of the graph path being traversed
      - explanation: plain English description of what the query finds
      - answerable: false if the question cannot be answered from the graph schema

    Example input:
      {
        "question": "Which gap topics always appear together?",
        "deployment_id": "dep-001"
      }
    """
    llm = get_llm()
    chunks = []
    for chunk in llm.stream([
        SystemMessage(content=CYPHER_QUERY_SYSTEM_PROMPT),
        HumanMessage(content=question_and_context),
    ]):
        token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
        print(token, end="", flush=True)
        chunks.append(token)
    return "".join(chunks).strip()
