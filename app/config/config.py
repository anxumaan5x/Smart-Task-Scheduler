import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("TS_DB_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
