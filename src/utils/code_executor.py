import os
import traceback
import datetime
import matplotlib
matplotlib.use("Agg")  # headless backend — must be set before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
from src.config.settings import OUTPUTS_DIR


def run_code(code: str) -> str:
    """Execute matplotlib code in an isolated namespace and save the chart."""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUTS_DIR, f"chart_{timestamp}.png")

    # Replace plt.show() so the chart is saved instead of displayed
    sanitized = code.replace(
        "plt.show()",
        f"plt.savefig(output_path, dpi=150, bbox_inches='tight')\nplt.close('all')",
    )
    if "plt.savefig" not in sanitized:
        sanitized += f"\nplt.savefig(output_path, dpi=150, bbox_inches='tight')\nplt.close('all')"

    exec_globals = {
        "__builtins__": __builtins__,
        "output_path": output_path,
        "plt": plt,
        "np": np,
    }

    try:
        exec(sanitized, exec_globals)  # noqa: S102
        if os.path.exists(output_path):
            return f"Chart saved to: {output_path}"
        return f"Code ran but no file found at: {output_path}"
    except Exception:
        return f"Execution error:\n{traceback.format_exc()}"
    finally:
        plt.close("all")
