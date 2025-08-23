from fastapi import FastAPI
from app.routes.agent_routes import router as agent_router

app = FastAPI()

app.include_router(agent_router, prefix="/agent", tags=["Agent"])


@app.get("/")
async def root():
    return {"message": "Welcome to Multi-Agent App 🚀"}