from langchain_core.tools import tool
from src.utils.code_executor import run_code


@tool
def execute_chart_code(code: str) -> str:
    """
    Execute Python matplotlib code to generate and save a chart.

    The execution scope pre-injects:
      - output_path (str): the file path where the chart will be saved
      - plt: matplotlib.pyplot
      - np: numpy

    The code should either call plt.savefig(output_path, ...) explicitly,
    or call plt.show() which is automatically replaced with a savefig call.

    Returns the saved file path on success, or an error traceback on failure.
    """
    return run_code(code)
