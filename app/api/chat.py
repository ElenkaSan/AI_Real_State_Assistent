from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from app.core.llm import get_response_with_rag

router = APIRouter()

# Request/Response schema
class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: List[Tuple[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    duration_ms: int

@router.post("/", response_model=ChatResponse)
async def chat_handler(req: ChatRequest):
    try:
        response, duration = get_response_with_rag(req.user_id, req.message, req.chat_history)
        return ChatResponse(response=response, duration_ms=duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))