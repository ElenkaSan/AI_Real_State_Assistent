from pydantic import BaseModel

from typing import List, Tuple

class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: List[Tuple[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    duration_ms: int