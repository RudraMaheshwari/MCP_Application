from fastmcp import FastMCP
from mcp.types import ImageContent
import json
from src.agents.chart_agent import run_chart_agent

mcp = FastMCP(name="Chart Generation MCP Server")


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


@mcp.resource("info://server")
def server_info() -> str:
    """Return metadata about this MCP server."""
    info = {
        "name": "chart-generation-mcp-server",
        "description": (
            "MCP server that uses a LangChain agent to generate matplotlib charts "
            "from natural language descriptions and returns them as inline images."
        ),
        "tools": ["generate_chart"],
        "supported_charts": ["bar", "histogram", "pie", "line", "scatter", "box", "heatmap"],
    }
    return json.dumps(info, indent=2)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
