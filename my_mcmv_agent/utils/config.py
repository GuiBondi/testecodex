"""Load environment variables and expose configuration values."""
import os
from dotenv import load_dotenv

# Load variables from .env located at project root
load_dotenv()

VIA_CEP_API_URL = os.getenv("VIA_CEP_API_URL")
DEMO_API_URL = os.getenv("DEMO_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

__all__ = [
    "VIA_CEP_API_URL",
    "DEMO_API_URL",
    "GEMINI_API_KEY",
    "GEMINI_API_ENDPOINT",
    "OPENAI_API_KEY",
    "GOOGLE_CLOUD_PROJECT",
]
