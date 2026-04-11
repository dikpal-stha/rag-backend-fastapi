from fastapi import APIRouter
from pydantic import BaseModel
from models.schemas import ChatRequest, ChatResponse
from services.booking import handle_booking_request
from services.rag import generate_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    booking_result = handle_booking_request(request.message, request.user_id)

    if booking_result["intent"] == "booking":
        return ChatResponse(
            response=booking_result["response"],
            intent="booking"
        )

    rag_response = generate_response(request.message, request.user_id)

    return ChatResponse(
        response=rag_response,
        intent="general"
    )