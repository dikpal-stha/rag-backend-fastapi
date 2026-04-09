from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Initialize Collection
COLLECTION_NAME = "documents"

# Initialize Model and Qdrant-client
def get_model():
    return (SentenceTransformer("all-MiniLM-L6-v2"))

# def get_client():
#     return (QdrantClient(url="http://localhost:6333"))

def get_client():
    qdrant_client = QdrantClient(
        url="https://493980df-1b84-467b-af74-2c16f6c71473.eu-central-1-0.aws.cloud.qdrant.io:6333", 
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6ZDZmNDlhNWItMDhhNC00ZWZmLTkxMDgtOWJiNDFkZDRiZTgzIn0.tiJ5J7lgy1ksFnT0JTjHE1-QhFl4MtTKiljybtlEnBI",
    )
    return qdrant_client
