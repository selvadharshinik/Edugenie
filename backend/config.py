import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "EduGenie"
    PROJECT_VERSION: str = "1.0.0"
    TAGLINE: str = "Your personal AI learning companion."

    @property
    def GEMINI_API_KEY(self) -> str:
        load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
        return os.getenv("GEMINI_API_KEY", "").strip()

    @property
    def PRIMARY_MODEL(self) -> str:
        load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
        return os.getenv("MODEL_NAME", "gemini-3.5-flash").strip()

    DEFAULT_TEMPERATURE: float = 0.7
    QUIZ_TEMPERATURE: float = 0.3
    MAX_OUTPUT_TOKENS: int = 2048

    TEMPLATES_DIR: Path = BASE_DIR / "frontend" / "templates"
    STATIC_DIR: Path = BASE_DIR / "frontend" / "static"

    @property
    def is_api_key_configured(self) -> bool:
        key = self.GEMINI_API_KEY
        return bool(key and key != "your_gemini_api_key_here")

settings = Settings()
