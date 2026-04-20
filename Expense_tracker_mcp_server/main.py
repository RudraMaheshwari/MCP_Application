import random
from fastmcp import FastMCP

#create a new MCP instance/ server
mcp=FastMCP(name="Demo MCP")

@mcp.tool #decorator to register the function as a tool
def roll_dice(sides: int = 1) -> list[int]:
    """Roll a dice with the given number of sides."""
    return [random.randint(1,6) for _ in range(sides)]

@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run() #to run the server
