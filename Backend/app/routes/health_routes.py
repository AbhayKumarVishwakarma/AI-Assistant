from fastapi import APIRouter, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.health_service import run_health_assistant
from app.auth.security import get_current_user


router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/ask", response_model=ChatResponse)
async def health_route(req: ChatRequest):
    resp = run_health_assistant(req.query)
    return ChatResponse(response=resp)