import re
import uuid
from loguru import logger
import os

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Configure logger with rotation, retention, and formatting
logger.add(
    "logs/real_estate_rag.log",
    rotation="1 MB",
    retention="7 days",
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)

# -------------------------
# UUID Generator
# -------------------------
def generate_uuid() -> str:
    try:
        return str(uuid.uuid4())
    except Exception as e:
        log_error(f"UUID generation failed: {e}")
        return str(uuid.uuid1())  # fallback

# -------------------------
# Text Cleaner
# -------------------------
def clean_text(text: str) -> str:
    # Remove unwanted characters, preserve useful punctuation
    text = re.sub(r"\s+", " ", text)  # normalize spaces
    text = re.sub(r"[^a-zA-Z0-9\s.,:/\-–—!?()\"']", "", text)  # allow common symbols
    return text.strip()

# -------------------------
# Logging Helpers
# -------------------------
def log_info(message: str, tag: str = ""):
    logger.info(f"{tag}: {message}" if tag else message)

def log_error(message: str, tag: str = ""):
    logger.error(f"{tag}: {message}" if tag else message)

def log_warn(message: str, tag: str = ""):
    logger.warning(f"{tag}: {message}" if tag else message)
