from fastmcp import FastMCP
import json
import os
from src.config.settings import OUTPUTS_DIR
from src.agents.chart_agent import run_chart_agent

mcp = FastMCP(name="Chart Generation MCP Server")


@mcp.tool
def generate_chart(description: str) -> str:
    """
    Generate a matplotlib chart from a natural language description and return the saved file path.

    Pass your data and chart type in plain English. Examples:
      - "Bar chart of monthly sales: Jan=5000, Feb=7200, Mar=6100"
      - "Pie chart of market share: Apple 30%, Samsung 25%, Others 45%"
      - "Histogram of ages: [22, 25, 29, 31, 35, 38, 40, 45]"
      - "Line chart showing temperature over a week: Mon=22, Tue=25, Wed=23"
      - "Scatter plot of height vs weight: [(160,55),(170,65),(180,80)]"

    Supported chart types: bar, histogram, pie, line, scatter, box, heatmap.
    """
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    return run_chart_agent(description)


@mcp.resource("info://server")
def server_info() -> str:
    """Return metadata about this MCP server."""
    info = {
        "name": "chart-generation-mcp-server",
        "description": (
            "MCP server that uses a LangChain agent to generate matplotlib charts "
            "from natural language descriptions."
        ),
        "tools": ["generate_chart"],
        "supported_charts": ["bar", "histogram", "pie", "line", "scatter", "box", "heatmap"],
        "outputs_dir": OUTPUTS_DIR,
    }
    return json.dumps(info, indent=2)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
