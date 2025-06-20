from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from .auth import get_current_user
from services.gemini_service import GeminiService
from services.firestore_service import FirestoreService

past_router = APIRouter()

class CaptureRequest(BaseModel):
    type: str  # "url", "text", "voice"
    content: str
    metadata: Optional[dict] = None

class CaptureResponse(BaseModel):
    id: str
    type: str
    content: str
    timestamp: datetime
    processed: bool
    summary: Optional[str] = None

class DigestResponse(BaseModel):
    captures: List[CaptureResponse]
    generated_at: datetime

@past_router.post("/capture", response_model=CaptureResponse)
async def capture_content(
    request: CaptureRequest,
    user = Depends(get_current_user)
):
    """コンテンツをキャプチャして保存"""
    firestore_service = FirestoreService()
    
    capture_data = {
        "user_id": user["uid"],
        "type": request.type,
        "content": request.content,
        "metadata": request.metadata or {},
        "timestamp": datetime.now(),
        "processed": False
    }
    
    capture_id = await firestore_service.save_capture(capture_data)
    
    return CaptureResponse(
        id=capture_id,
        type=request.type,
        content=request.content,
        timestamp=capture_data["timestamp"],
        processed=False
    )

@past_router.get("/digest", response_model=DigestResponse)
async def get_digest(user = Depends(get_current_user)):
    """処理済みのキャプチャを取得（朝のダイジェスト）"""
    firestore_service = FirestoreService()
    
    captures = await firestore_service.get_processed_captures(user["uid"])
    
    return DigestResponse(
        captures=captures,
        generated_at=datetime.now()
    )

@past_router.post("/process-batch")
async def process_batch():
    """バッチ処理用エンドポイント（夜間処理）"""
    firestore_service = FirestoreService()
    gemini_service = GeminiService()
    
    unprocessed_captures = await firestore_service.get_unprocessed_captures()
    
    processed_count = 0
    for capture in unprocessed_captures:
        try:
            if capture["type"] == "url":
                summary = await gemini_service.summarize_url(capture["content"])
            elif capture["type"] == "text":
                summary = await gemini_service.summarize_text(capture["content"])
            else:
                continue
                
            await firestore_service.update_capture_summary(capture["id"], summary)
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing capture {capture['id']}: {e}")
            continue
    
    return {"processed_count": processed_count}