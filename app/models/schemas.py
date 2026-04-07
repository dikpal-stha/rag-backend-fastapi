from pydantic import BaseModel
from typing import Optional

# class ChatRequest(BaseModel):
#     user_id: str
#     query: str

class BookingDetails(BaseModel):
    intent: str
    name: Optional[str] = None
    email: Optional[str] = None
    Date: Optional[str] = None
    time: Optional[str] = None



