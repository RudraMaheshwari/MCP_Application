from langchain_core.tools import tool
from src.utils.code_executor import run_code


@tool
def execute_chart_code(code: str) -> str:
    """
    Execute Python matplotlib code to generate a chart.

    The execution scope pre-injects:
      - plt: matplotlib.pyplot
      - np: numpy

    Do NOT call plt.savefig(), plt.show(), or plt.close() — the executor
    captures the figure automatically and returns it as a base64 PNG string.

    Returns a base64-encoded PNG string on success, or an error traceback on failure.
    """
    return run_code(code)
