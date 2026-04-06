from fastapi import APIRouter
from pydantic import BaseModel
from services.rag import generate_response

router = APIRouter()

# request schema
class ChatRequest(BaseModel):
    user_id: str
    query: str


@router.post('/')
def chat(req: ChatRequest):
    response = generate_response(req.query, req.user_id)

    return {"response": response}



    