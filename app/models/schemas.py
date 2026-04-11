from pydantic import BaseModel
from typing import Optional


class BookingDetails(BaseModel):
    intent: str
    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None


class ChatRequest(BaseModel):
    user_id: str
    query: str


class ChatResponse(BaseModel):
    response: str
    intent: str
