from typing import List, Dict
from core.config import get_client, get_model, COLLECTION_NAME
from qdrant_client.http.models import VectorParams, PointStruct

# Initialize Model and Qdrant-client
model = get_model()
client = get_client()

# check if the collection exists
if COLLECTION_NAME not in [c.name for c in client.get_collection().collections]:
    client.recreate_collection(
        collection_name = COLLECTION_NAME,
        vectors_config  = VectorParams(size=384, distance="Cosine")
        )

# embedding generation
def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    embeddings = model.encode(chunks)

    return embeddings.tolist()

# Upsert chunks to Qdrant
def store_chunks(chunks: List[str], metadata: List[Dict]):
    embeddings = generate_embeddings(chunks)

    points = [
        PointStruct(id=i, vector=vec, payload=meta)
        for i, (vec,meta) in enumerate(zip(embeddings, metadata))
    ]

    client.upsert(collection_name= COLLECTION_NAME, points = points)














# -----------------------------
# Querying chunks
# -----------------------------
# def search_chunks(query: str, top_k: int = 5):
#     query_vec = model.encode([query])[0].tolist()
#     scroll_result, _ = client.scroll(collection_name=COLLECTION_NAME, limit=1000)
#     all_points = [p for p in scroll_result if p.vector is not None]

#     def cosine_sim(a, b):
#         a = np.array(a)
#         b = np.array(b)
#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#     sims = [(p.payload, cosine_sim(query_vec, p.vector)) for p in all_points]
#     sims.sort(key=lambda x: x[1], reverse=True)
#     return sims[:top_k]


