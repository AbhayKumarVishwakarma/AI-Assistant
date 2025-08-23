from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.health_service import run_health_assistant


router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
async def health_route(req: ChatRequest):
    resp = run_health_assistant(req.query)
    return ChatResponse(response=resp)