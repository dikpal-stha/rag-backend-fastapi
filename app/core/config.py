from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Initialize Collection
COLLECTION_NAME = "documents"

# Initialize Model and Qdrant-client
def get_model():
    return (SentenceTransformer("all-MiniLM-L6-v2"))

def get_client():
    return (QdrantClient(url="http://localhost:6333"))