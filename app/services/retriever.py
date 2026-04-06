from core.config import get_client, get_model, COLLECTION_NAME
from typing import List, Dict

# Initialize model and client
model = get_model()
client = get_client()

# Qdrant retriever
def retrieve_chunks(query: str, top_k: int = 3)-> List[Dict]:

    # Convert query into embeddings
    query_vector = model.encode([query])[0].tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = top_k
    )

    # Return payloads (metadata)
    return [res.payload for res in results.points]

