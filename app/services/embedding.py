import uuid
from typing import List, Dict
from core.config import COLLECTION_NAME
from core.clients import get_qdrant_client
from core.model_loader import get_embedding_model
from qdrant_client.http.models import VectorParams, PointStruct

# Get Embedding Model and Qdrant-client
emd_model = get_embedding_model()
client = get_qdrant_client()

# check if the collection exists
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name = COLLECTION_NAME,
        vectors_config  = VectorParams(size=384, distance="Cosine")
        )

# embedding generation
def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    embeddings = emd_model.encode(chunks)

    return embeddings.tolist()

# Upsert chunks to Qdrant
def store_chunks(chunks: List[str], metadata: List[Dict]):
    embeddings = generate_embeddings(chunks)

    points = [
        PointStruct(id= str(uuid.uuid4()), vector=vec, payload=meta)
        for vec, meta in zip(embeddings, metadata)
    ]

    client.upsert(collection_name= COLLECTION_NAME, points = points)




