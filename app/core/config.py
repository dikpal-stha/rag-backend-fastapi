import os
from dotenv import load_dotenv

load_dotenv()

# LLM Models
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "google/flan-t5-base")

# Qdrant config
USE_LOCAL_QDRANT = os.getenv("USE_LOCAL_QDRANT", "false").lower() == "true"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Redis config
USE_LOCAL_REDIS = os.getenv("USE_LOCAL_REDIS", "false").lower() == "true"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_USERNAME = os.getenv("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# DB / collection
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
DB_PATH = os.getenv("DB_PATH", "metadata.db")
BOOKING_DB_PATH = os.getenv("BOOKING_DB_PATH", "bookings.db")