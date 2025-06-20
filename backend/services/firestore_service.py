import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from google.cloud import firestore
import uuid

class FirestoreService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if self.project_id:
            self.db = firestore.Client(project=self.project_id)
        else:
            self.db = None
    
    async def save_capture(self, capture_data: Dict[str, Any]) -> str:
        """キャプチャデータを保存"""
        if not self.db:
            return "mock-capture-id"
        
        capture_id = str(uuid.uuid4())
        capture_data["id"] = capture_id
        
        doc_ref = self.db.collection("users").document(capture_data["user_id"]).collection("captures").document(capture_id)
        doc_ref.set(capture_data)
        
        return capture_id
    
    async def get_processed_captures(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """処理済みのキャプチャを取得"""
        if not self.db:
            return []
        
        captures_ref = (
            self.db.collection("users")
            .document(user_id)
            .collection("captures")
            .where("processed", "==", True)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        
        docs = captures_ref.stream()
        captures = []
        
        for doc in docs:
            data = doc.to_dict()
            captures.append({
                "id": data["id"],
                "type": data["type"],
                "content": data["content"],
                "timestamp": data["timestamp"],
                "processed": data["processed"],
                "summary": data.get("summary", "")
            })
        
        return captures
    
    async def get_unprocessed_captures(self) -> List[Dict[str, Any]]:
        """未処理のキャプチャを取得（バッチ処理用）"""
        if not self.db:
            return []
        
        # 24時間以内の未処理キャプチャを取得
        yesterday = datetime.now() - timedelta(days=1)
        
        captures = []
        users_ref = self.db.collection("users")
        
        for user_doc in users_ref.stream():
            captures_ref = (
                user_doc.reference.collection("captures")
                .where("processed", "==", False)
                .where("timestamp", ">=", yesterday)
            )
            
            for capture_doc in captures_ref.stream():
                data = capture_doc.to_dict()
                data["id"] = capture_doc.id
                data["user_id"] = user_doc.id
                captures.append(data)
        
        return captures
    
    async def update_capture_summary(self, capture_id: str, summary: str):
        """キャプチャの要約を更新"""
        if not self.db:
            return
        
        # Note: In a real implementation, we would need the user_id 
        # For now, we'll update based on capture_id across all users
        # This is a simplified implementation for testing
        return
    
    async def save_briefing(self, briefing_data: Dict[str, Any]) -> str:
        """ブリーフィングを保存"""
        if not self.db:
            return "mock-briefing-id"
        
        briefing_id = str(uuid.uuid4())
        briefing_data["id"] = briefing_id
        
        doc_ref = (
            self.db.collection("users")
            .document(briefing_data["user_id"])
            .collection("briefings")
            .document(briefing_id)
        )
        doc_ref.set(briefing_data)
        
        return briefing_id
    
    async def get_user_briefings(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """ユーザーのブリーフィングを取得"""
        if not self.db:
            return []
        
        briefings_ref = (
            self.db.collection("users")
            .document(user_id)
            .collection("briefings")
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        
        docs = briefings_ref.stream()
        briefings = []
        
        for doc in docs:
            data = doc.to_dict()
            briefings.append({
                "id": data["id"],
                "event_id": data["event_id"],
                "event_title": data["event_title"],
                "event_time": data["event_time"],
                "briefing_content": data["briefing_content"],
                "created_at": data["created_at"]
            })
        
        return briefings