import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


class Settings:

    BASE_DIR = BASE_DIR

    PROJECT_NAME = "ResponsibleMetrics AI"

    PROJECT_VERSION = "1.0.0"

    UPLOAD_DIR = os.path.join(
        BASE_DIR,
        "uploads"
    )

    OPENALEX_BASE_URL = "https://api.openalex.org"

    OPENALEX_EMAIL = os.getenv(
        "OPENALEX_EMAIL",
        ""
    )


settings = Settings()