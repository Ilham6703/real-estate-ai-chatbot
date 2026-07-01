import os

from backend.app.config import settings

os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY

os.environ["LANGSMITH_TRACING"] = str(
    settings.LANGSMITH_TRACING
).lower()

os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT