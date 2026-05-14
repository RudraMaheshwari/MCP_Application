from fastmcp import FastMCP
from mcp.types import ImageContent
import json
from src.agents.chart_agent import run_chart_agent
from src.agents.knowledge_extraction_agent import run_knowledge_extraction_agent
from src.agents.knowledge_gap_agent import run_knowledge_gap_agent
from src.agents.report_generator_agent import run_report_generator_agent
from src.agents.gap_report_agent import run_gap_report_agent
from src.agents.alert_monitor_agent import run_alert_monitor_agent
from src.agents.sql_executor_agent import run_sql_executor_agent
from src.agents.vector_search_agent import run_vector_search_agent
from src.agents.cypher_query_agent import run_cypher_query_agent
from src.agents.transcript_drilldown_agent import run_transcript_drilldown_agent

mcp = FastMCP(name="Intelligence MCP Server")


@mcp.tool
def generate_chart(description: str) -> list[ImageContent]:
    """
    Generate a matplotlib chart from a natural language description and return it as an image.

    Pass your data and chart type in plain English. Examples:
      - "Bar chart of monthly sales: Jan=5000, Feb=7200, Mar=6100"
      - "Pie chart of market share: Apple 30%, Samsung 25%, Others 45%"
      - "Histogram of ages: [22, 25, 29, 31, 35, 38, 40, 45]"
      - "Line chart showing temperature over a week: Mon=22, Tue=25, Wed=23"
      - "Scatter plot of height vs weight: [(160,55),(170,65),(180,80)]"

    Supported chart types: bar, histogram, pie, line, scatter, box, heatmap.
    Returns the chart as an inline image.
    """
    b64 = run_chart_agent(description)

    if b64.startswith("ERROR"):
        raise ValueError(b64)

    return [ImageContent(type="image", data=b64, mimeType="image/png")]


@mcp.tool
def extract_knowledge(text: str) -> str:
    """
    Extract structured knowledge from any text (transcript, document, conversation).

    Returns a JSON object with:
      - entities (people, orgs, products, concepts, locations)
      - facts with confidence levels (high / medium / low)
      - key topics
      - action items with owners and due dates
      - relationships between entities
      - one-sentence summary

    Pass the raw text directly. Examples:
      - A meeting transcript to pull out decisions and action items
      - A support conversation to identify mentioned products and issues
      - An article to extract key facts and entities
    """
    result = run_knowledge_extraction_agent(text)
    return json.dumps(result, indent=2)


@mcp.tool
def detect_knowledge_gaps(text: str) -> str:
    """
    Detect knowledge gaps, ambiguities, and missing information in any text.

    Returns a JSON object with:
      - unanswered_questions with severity (critical / major / minor)
      - missing_information topics
      - ambiguities with explanations
      - incomplete_topics with expansion suggestions
      - suggested_followups (up to 5 actionable questions)
      - overall_completeness_score (0–100)
      - one-sentence gap summary

    Pass the raw text directly. Examples:
      - A meeting transcript to find unresolved questions
      - A requirements document to spot missing specs
      - A support conversation to identify open issues
    """
    result = run_knowledge_gap_agent(text)
    return json.dumps(result, indent=2)


@mcp.tool
def generate_period_report(aggregated_data: str) -> str:
    """
    Generate a structured executive report from pre-aggregated call performance data.

    Accepts a JSON string with call volume, avg QA score, avg sentiment, top issues,
    compliance findings, knowledge gaps, and write-back outcomes for a time period.

    Returns a JSON report with all the above fields plus a narrative executive summary
    and a report_health signal (green / amber / red).
    """
    result = run_report_generator_agent(aggregated_data)
    return json.dumps(result, indent=2)


@mcp.tool
def generate_gap_report(gaps_data: str) -> str:
    """
    Generate a prioritised knowledge gap report for the Prep team.

    Accepts a JSON string with knowledge gaps detected across multiple sessions —
    each gap has topic, canonical_question, frequency, suggested_action, and sample_session_ids.

    Returns a JSON report with gaps grouped by topic, ranked by frequency,
    critical_gaps list, action_breakdown, overall_health (green / amber / red),
    and a one-sentence summary of the most urgent gap cluster.

    suggested_action values:
      - add_to_knowledge    : answer missing from knowledge base
      - clarify_policy      : policy is ambiguous
      - add_tool            : no tool exists for this question
      - escalate_to_human_only : outside AI scope by design
    """
    result = run_gap_report_agent(gaps_data)
    return json.dumps(result, indent=2)


@mcp.tool
def monitor_alerts(summary_and_thresholds: str) -> str:
    """
    Evaluate a PostCallSummary against configured thresholds and determine which alerts to fire.

    Accepts a JSON string with:
      - post_call_summary: the full PostCallSummary for one session
      - thresholds: min_qa_score and max_gaps_per_session for this deployment

    Alert types detected:
      - qa_drop            : QA score below threshold
      - compliance_finding : any no_policy_breach rule returned fail
      - sentiment_spike    : overall sentiment is very_negative
      - gap_surge          : knowledge gaps count exceeds threshold

    Returns a JSON object with alerts_fired list, no_alerts_fired flag,
    call_health, and a one-sentence summary.
    """
    result = run_alert_monitor_agent(summary_and_thresholds)
    return json.dumps(result, indent=2)


@mcp.tool
def execute_nl_to_sql(question_and_context: str) -> str:
    """
    Convert a natural language question into a parameterised SQL query for the post-call analytics database.

    Accepts a JSON string with question, deployment_id, and optional context.
    Always generates SELECT-only queries with deployment_id injected for RBAC.

    Returns a JSON object with generated_sql, parameters, expected_columns,
    explanation, and answerable flag.

    Best for: counts, filters, rankings, time ranges, aggregations over call data.
    """
    result = run_sql_executor_agent(question_and_context)
    return json.dumps(result, indent=2)


@mcp.tool
def semantic_search(query_and_documents: str) -> str:
    """
    Perform semantic similarity search over PostCallSummary key_facts.

    Accepts a JSON string with a natural language query and a list of PostCallSummary
    documents (each with session_id and key_facts array).

    Returns a JSON object with matches ranked by relevance_score (0.0–1.0),
    matched_key_facts, explanations, and reformulations_used for broader recall.

    Best for: meaning-based search — finds "frustrated with shipping" when you search
    "angry about delivery", even with no shared keywords.
    """
    result = run_vector_search_agent(query_and_documents)
    return json.dumps(result, indent=2)


@mcp.tool
def generate_cypher_query(question_and_context: str) -> str:
    """
    Convert a natural language question about graph relationships into a Neo4j Cypher query.

    Accepts a JSON string with question, deployment_id, and optional context.
    Generates read-only MATCH ... RETURN queries against the knowledge graph.

    Graph contains: Session, Gap, Topic, Customer, Policy nodes with
    REVEALED, BELONGS_TO, HAD, RAN_WITH, TRACES_TO edges.

    Returns a JSON object with generated_cypher, parameters, traversal_pattern,
    explanation, and answerable flag.

    Best for: co-occurrence patterns, customer repeat gaps, policy root-cause clustering.
    """
    result = run_cypher_query_agent(question_and_context)
    return json.dumps(result, indent=2)


@mcp.tool
def drilldown_transcript(query_and_transcript: str) -> str:
    """
    Extract and summarise the most relevant turns from a call transcript for a given topic.

    Accepts a JSON string with session_id, a search query or topic, and the transcript
    turns (each with turn_index, speaker, and content).

    Returns a JSON object with relevant_turns (verbatim), context_turns (2 before/after
    each relevant turn), a 2–3 sentence summary, and sentiment_at_section.

    Use this to drill into a specific session after a broader search has identified it,
    or to fetch transcript context behind a citation in an insight answer.
    """
    result = run_transcript_drilldown_agent(query_and_transcript)
    return json.dumps(result, indent=2)


@mcp.resource("info://server")
def server_info() -> str:
    """Return metadata about this MCP server."""
    info = {
        "name": "intelligence-mcp-server",
        "description": (
            "MCP server with LangChain agents for post-call intelligence: "
            "chart generation, knowledge extraction, knowledge gap detection, "
            "period report generation, gap report generation, alert monitoring, "
            "SQL query generation, semantic search, Cypher query generation, "
            "and transcript drill-down."
        ),
        "tools": [
            "generate_chart",
            "extract_knowledge",
            "detect_knowledge_gaps",
            "generate_period_report",
            "generate_gap_report",
            "monitor_alerts",
            "execute_nl_to_sql",
            "semantic_search",
            "generate_cypher_query",
            "drilldown_transcript",
        ],
        "supported_charts": ["bar", "histogram", "pie", "line", "scatter", "box", "heatmap"],
    }
    return json.dumps(info, indent=2)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
