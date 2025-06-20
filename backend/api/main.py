from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import auth_router
from .past_mode import past_router
from .future_mode import future_router

app = FastAPI(
    title="Janus AI Butler API",
    description="双貌のAI執事 - Past & Future Mode API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(past_router, prefix="/past", tags=["past-mode"])
app.include_router(future_router, prefix="/future", tags=["future-mode"])

@app.get("/")
async def root():
    return {"message": "Janus AI Butler API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "janus-ai-butler"}