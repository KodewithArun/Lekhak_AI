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

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
RITEKIT_API_KEY = os.getenv("RITEKIT_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

APP_NAME = os.getenv("APP_NAME", "agents")
USER_ID = os.getenv("USER_ID", "streamlit_user")
DB_URL = os.getenv("DB_URL")
