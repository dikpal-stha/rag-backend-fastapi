import redis
from qdrant_client import QdrantClient
from core.config import (
    USE_LOCAL_QDRANT,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_URL,
    QDRANT_API_KEY,
    USE_LOCAL_REDIS, 
    REDIS_HOST, 
    REDIS_PORT, 
    REDIS_USERNAME, 
    REDIS_PASSWORD
)

_qdrant_client = None
_redis_client = None

def get_qdrant_client():
    global _qdrant_client

    if _qdrant_client is None:
        if USE_LOCAL_QDRANT:
            _qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        else:
             _qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def get_redis_client():
    global _redis_client

    if _redis_client is None:
        if USE_LOCAL_REDIS:
            _redis_client = redis.Redis(
                host=REDIS_HOST, 
                port=REDIS_PORT, 
                decode_responses=True
                )

        else:
            _redis_client = redis.Redis(
                host=REDIS_HOST, 
                port=REDIS_PORT, 
                username=REDIS_USERNAME, 
                password=REDIS_PASSWORD, 
                decode_responses=True
                )

