from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Janus AI Butler API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "janus-ai-butler"}

@app.post("/test/capture")
async def test_capture(data: dict):
    """テスト用のキャプチャエンドポイント"""
    return {
        "id": "test-capture-123",
        "type": data.get("type", "url"),
        "content": data.get("content", ""),
        "timestamp": "2024-01-01T00:00:00",
        "processed": False
    }