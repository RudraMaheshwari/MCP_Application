from fastmcp import FastMCP
import random
import json

mcp = FastMCP(name="Expense Tracker MCP Server")

@mcp.tool #decorator to register the function as a tool
def roll_dice(sides: int = 1) -> list[int]:
    """Roll a dice with the given number of sides."""
    return [random.randint(1,6) for _ in range(sides)]

@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.resource("info://server")
def server_info() -> str:
    """Return information about the server."""
    info = {
        "name": "simple-expense-tracker-mcp-server",
        "description": "This server provides tools for rolling dice and adding numbers.",
        "tools": ["add_numbers", "roll_dice"]
    }
    return json.dumps(info, indent =2)

if __name__ == "__main__":
   mcp.run(transport="http", host = "0.0.0.0",port=8001)