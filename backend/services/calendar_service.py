import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarService:
    def __init__(self):
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Google Calendar APIサービスを初期化"""
        try:
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if credentials_path:
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=['https://www.googleapis.com/auth/calendar.readonly']
                )
                self.service = build('calendar', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Calendar service initialization failed: {e}")
            self.service = None
    
    async def get_upcoming_events(self, user_id: str, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """今後の予定を取得"""
        if not self.service:
            return []
        
        try:
            # 現在時刻から指定日数後まで
            now = datetime.utcnow()
            end_time = now + timedelta(days=days_ahead)
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # イベント情報を整形
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                formatted_event = {
                    'id': event['id'],
                    'summary': event.get('summary', 'No title'),
                    'description': event.get('description', ''),
                    'start': start,
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'attendees': event.get('attendees', []),
                    'location': event.get('location', ''),
                    'created': event.get('created', ''),
                    'updated': event.get('updated', '')
                }
                formatted_events.append(formatted_event)
            
            return formatted_events
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    async def get_event(self, user_id: str, event_id: str) -> Optional[Dict[str, Any]]:
        """特定のイベントを取得"""
        if not self.service:
            return None
        
        try:
            event = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            return {
                'id': event['id'],
                'summary': event.get('summary', 'No title'),
                'description': event.get('description', ''),
                'start': event['start'],
                'end': event['end'],
                'attendees': event.get('attendees', []),
                'location': event.get('location', ''),
                'created': event.get('created', ''),
                'updated': event.get('updated', '')
            }
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    async def get_events_for_briefing(self, user_id: str, hours_ahead: int = 24) -> List[Dict[str, Any]]:
        """ブリーフィング対象の予定を取得"""
        if not self.service:
            return []
        
        try:
            # 現在時刻から指定時間後まで
            now = datetime.utcnow()
            end_time = now + timedelta(hours=hours_ahead)
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                maxResults=20,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # 会議室予約などではなく、実際の会議や重要な予定のみを対象とする
            important_events = []
            for event in events:
                # 参加者がいる、または説明がある場合は重要な予定とみなす
                if event.get('attendees') or event.get('description'):
                    important_events.append({
                        'id': event['id'],
                        'summary': event.get('summary', 'No title'),
                        'description': event.get('description', ''),
                        'start': event['start'],
                        'end': event['end'],
                        'attendees': event.get('attendees', []),
                        'location': event.get('location', ''),
                    })
            
            return important_events
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []