from pydantic import BaseModel
from typing import Optional


class BookingDetails(BaseModel):
    intent: str
    name: Optional[str] = None
    email: Optional[str] = None
    Date: Optional[str] = None
    time: Optional[str] = None



