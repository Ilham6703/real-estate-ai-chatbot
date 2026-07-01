"""
Application configuration.

All environment variables are loaded from the project's .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings.
    """

    # =====================================================
    # AI Provider
    # =====================================================

    LLM_PROVIDER: str = "openai"

    # =====================================================
    # Gemini
    # =====================================================

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-001"

    # =====================================================
    # OpenAI (Optional)
    # =====================================================

    OPENAI_API_KEY: str = ""

    OPENAI_CHAT_MODEL: str = "gpt-4.1-mini"

    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    # =====================================================
    # Grok / xAI (Optional)
    # =====================================================

    XAI_API_KEY: str = ""

    # =====================================================
    # Mistral (Optional)
    # =====================================================

    MISTRAL_API_KEY: str = ""

    # =====================================================
    # Qdrant
    # =====================================================

    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "real_estate_chatbot"

    # =====================================================
    # LangSmith
    # =====================================================

    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: bool = False
    LANGSMITH_PROJECT: str = "real-estate-chatbot"

    # =====================================================
    # Google Sheets
    # =====================================================

    GOOGLE_SHEET_ID: str = ""
    GOOGLE_SERVICE_ACCOUNT_FILE: str = ""

    # =====================================================
    # FastAPI
    # =====================================================

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # =====================================================
    # Frontend
    # =====================================================

    FRONTEND_URL: str = "http://127.0.0.1:5500"

    # =====================================================
    # Settings
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()