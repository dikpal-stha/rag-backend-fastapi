# RAG-based Chat & Booking System

## Overview
This project includes:
- RAG for answering user queries
- Redis-based memory for multi-turn query and interview booking
- Qdrant vector database for document retrieval

The system supports both general chat queries and interview booking.


## Features
- Multi-turn queries support using Redis memory
- Hybrid booking extraction (regex + LLM)
- SQL storage for meta-data and booking
- Selectable chunking methods for document ingestion
- Vector search (Qdrant)


## Tech Stack
- Python
- FastAPI
- Qdrant (Vector DB)
- Redis (Memory)
- SQLite (Booking storage)
- SentenceTransformers (Embeddings)
- HuggingFace Transformers (LLM)


## Project Structure

app/
│
├── core/          # Config, clients, model_loader
├── services/      # RAG, booking, memory, retriever
├── models/        # Pydantic schemas
├── routes/        # API endpoints
├── main.py        # Entry point


## How It Works

1. User sends a query via API
2. System detects intent (booking or general query)
3. If booking:
   - Extract fields (name, email, date, time)
   - Store state in Redis
   - Ask for missing fields
   - Save to SQLite when complete
4. If general query:
   - Retrieve relevant documents from Qdrant
   - Build context
   - Generate response using LLM
5. Chat history is stored in Redis for multi-turn interaction


## Setup

1. Create virtual environment:
   python -m venv venv

2. Activate:
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create `.env` file based on `.env.example`

5. Run server:
   uvicorn app.main:app --reload


## API Usage

POST /chat

Request:
{
  "user_id": "test1",
  "query": "I want to book an appointment"
}

Supports:
- General RAG queries
- Multi-turn booking interactions


## Limitations

- LLM (Flan-T5) is weak and inconsistent, so it might hallucinate


## Future Improvements

- Use stronger LLM model(For ex. Qwen)
- Improve booking extraction
- Reduce LLM hallucination



P.S Tested on google colab cause of system limitation(win 7) 
