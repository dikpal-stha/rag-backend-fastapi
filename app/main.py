from fastapi import FASTAPI
from app.routes import ingestion, chat

app = FASTAPI(
    title = "RAG Internship Project",
    description = "Data ingestion API + chat RAG API",
    version = "0.1",
)

# Routers
app.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])






