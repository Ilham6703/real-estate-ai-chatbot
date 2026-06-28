from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from the .env file.
    """

    # =====================================================
    # LLM Configuration
    # =====================================================

    LLM_PROVIDER: str = "gemini"

    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    XAI_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""

    # =====================================================
    # Qdrant Configuration
    # =====================================================

    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION: str = "real_estate_chatbot"

    # =====================================================
    # LangSmith Configuration
    # =====================================================

    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: bool = True
    LANGSMITH_PROJECT: str = "real-estate-chatbot"

    # =====================================================
    # Google Sheets Configuration
    # =====================================================

    GOOGLE_SHEET_ID: str = ""
    GOOGLE_SERVICE_ACCOUNT_FILE: str = "credentials.json"

    # =====================================================
    # FastAPI Configuration
    # =====================================================

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Load variables from the root .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()