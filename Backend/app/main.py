from fastapi import FastAPI
from app.routes import agent_routes, health_routes

app = FastAPI()

app.include_router(agent_routes.router, prefix="/agent", tags=["Agent"])
app.include_router(health_routes.router, prefix="/health", tags=["Health Assistant"])


@app.get("/")
async def root():
    return {"message": "Welcome to Multi-Agent App 🚀"}