import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Google API configuration as environment variables for ADK
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set environment variables so ADK can pick them up
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(GOOGLE_GENAI_USE_VERTEXAI)
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

APP_NAME = os.getenv("APP_NAME", "agents")
USER_ID = os.getenv("USER_ID", "streamlit_user")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "lekhak_ai")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# ADK requires asyncpg driver, but both write to same PostgreSQL database
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Sync URL for SQLAlchemy CRUD operations (uses psycopg2 for synchronous queries)
DATABASE_URL_SYNC = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
