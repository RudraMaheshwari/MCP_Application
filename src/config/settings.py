from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY") or os.environ["OPENAPI_API_KEY"]
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
OUTPUTS_DIR: str = os.getenv("OUTPUTS_DIR", "outputs")
