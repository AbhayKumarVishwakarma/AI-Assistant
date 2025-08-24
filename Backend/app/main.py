from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import agent_routes, health_routes, user_routes, auth_routes

app = FastAPI(title="Multi-Agent App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_routes.router, prefix="/agent", tags=["Agent"])
app.include_router(health_routes.router, prefix="/health", tags=["Health Assistant"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to Multi-Agent App 🚀"}