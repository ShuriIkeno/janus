from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from .auth import get_current_user
from services.calendar_service import CalendarService
from services.gemini_service import GeminiService
from services.firestore_service import FirestoreService

future_router = APIRouter()

class BriefingRequest(BaseModel):
    event_id: str
    hours_before: int = 24

class BriefingResponse(BaseModel):
    id: str
    event_id: str
    event_title: str
    event_time: datetime
    briefing_content: str
    created_at: datetime

class UpcomingEventsResponse(BaseModel):
    events: List[dict]
    retrieved_at: datetime

@future_router.get("/upcoming-events", response_model=UpcomingEventsResponse)
async def get_upcoming_events(
    days_ahead: int = 7,
    user = Depends(get_current_user)
):
    """今後の予定を取得"""
    calendar_service = CalendarService()
    
    events = await calendar_service.get_upcoming_events(
        user["uid"], 
        days_ahead=days_ahead
    )
    
    return UpcomingEventsResponse(
        events=events,
        retrieved_at=datetime.now()
    )

@future_router.post("/generate-briefing", response_model=BriefingResponse)
async def generate_briefing(
    request: BriefingRequest,
    user = Depends(get_current_user)
):
    """特定のイベントに対するブリーフィングを生成"""
    calendar_service = CalendarService()
    gemini_service = GeminiService()
    firestore_service = FirestoreService()
    
    # イベント詳細を取得
    event = await calendar_service.get_event(user["uid"], request.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # ブリーフィング生成
    briefing_content = await gemini_service.generate_briefing(event)
    
    # 保存
    briefing_data = {
        "user_id": user["uid"],
        "event_id": request.event_id,
        "event_title": event["summary"],
        "event_time": event["start"]["dateTime"],
        "briefing_content": briefing_content,
        "created_at": datetime.now()
    }
    
    briefing_id = await firestore_service.save_briefing(briefing_data)
    
    return BriefingResponse(
        id=briefing_id,
        event_id=request.event_id,
        event_title=event["summary"],
        event_time=datetime.fromisoformat(event["start"]["dateTime"]),
        briefing_content=briefing_content,
        created_at=briefing_data["created_at"]
    )

@future_router.get("/briefings", response_model=List[BriefingResponse])
async def get_briefings(user = Depends(get_current_user)):
    """ユーザーのブリーフィング一覧を取得"""
    firestore_service = FirestoreService()
    
    briefings = await firestore_service.get_user_briefings(user["uid"])
    
    return [
        BriefingResponse(
            id=b["id"],
            event_id=b["event_id"],
            event_title=b["event_title"],
            event_time=b["event_time"],
            briefing_content=b["briefing_content"],
            created_at=b["created_at"]
        )
        for b in briefings
    ]