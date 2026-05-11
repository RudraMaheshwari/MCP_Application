import io
import re
import base64
import traceback
import matplotlib
matplotlib.use("Agg")  # headless backend — must be set before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def run_code(code: str) -> str:
    """Execute matplotlib or plotly code and return the chart as a base64-encoded PNG."""
    # Strip display/save calls — executor captures the figure itself
    sanitized = re.sub(r'plt\.savefig\([^)]*\)', '', code)
    sanitized = re.sub(r'plt\.show\(\)', '', sanitized)
    sanitized = re.sub(r'plt\.close\([^)]*\)', '', sanitized)
    sanitized = re.sub(r'fig\.show\(\)', '', sanitized)
    sanitized = re.sub(r'fig\.write_image\([^)]*\)', '', sanitized)

    exec_globals = {
        "__builtins__": __builtins__,
        "plt": plt,
        "np": np,
        "px": px,
        "go": go,
        "pd": pd,
    }

    try:
        exec(sanitized, exec_globals)  # noqa: S102

        buf = io.BytesIO()
        fig = exec_globals.get("fig")

        if fig is not None and hasattr(fig, "write_image"):
            # Plotly figure — high-res export via kaleido
            fig.write_image(buf, format="png", scale=2, width=1200, height=700)
        else:
            # Matplotlib figure
            plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")

        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    except Exception:
        return f"ERROR:\n{traceback.format_exc()}"
    finally:
        plt.close("all")
