import os
from typing import Optional
import vertexai
from vertexai.generative_models import GenerativeModel
import httpx
from bs4 import BeautifulSoup

class GeminiService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = "asia-northeast1"
        
        if self.project_id:
            vertexai.init(project=self.project_id, location=self.location)
            self.model = GenerativeModel("gemini-1.5-pro")
        else:
            self.model = None
    
    async def summarize_url(self, url: str) -> str:
        """URLの内容を要約"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            text = soup.get_text()
            text = ' '.join(text.split())
            
            if len(text) > 5000:
                text = text[:5000] + "..."
            
            prompt = f"""
            以下のWebページの内容を日本語で簡潔に要約してください。
            - 重要なポイントを3つ以内で整理
            - 各ポイントは1-2文で説明
            - 読みやすい箇条書き形式で出力
            
            URL: {url}
            
            内容:
            {text}
            """
            
            if self.model:
                response = self.model.generate_content(prompt)
                return response.text
            else:
                return f"URL: {url}\n内容の要約が利用できません（Gemini APIが設定されていません）"
                
        except Exception as e:
            return f"URL: {url}\n要約中にエラーが発生しました: {str(e)}"
    
    async def summarize_text(self, text: str) -> str:
        """テキストを要約"""
        try:
            prompt = f"""
            以下のテキストを日本語で簡潔に要約してください。
            - 重要なポイントを3つ以内で整理
            - 各ポイントは1-2文で説明
            - 読みやすい箇条書き形式で出力
            
            テキスト:
            {text}
            """
            
            if self.model:
                response = self.model.generate_content(prompt)
                return response.text
            else:
                return f"テキストの要約が利用できません（Gemini APIが設定されていません）\n\n元のテキスト: {text[:200]}..."
                
        except Exception as e:
            return f"要約中にエラーが発生しました: {str(e)}"
    
    async def generate_briefing(self, event: dict) -> str:
        """カレンダーイベントに基づいてブリーフィングを生成"""
        try:
            event_title = event.get("summary", "")
            event_description = event.get("description", "")
            attendees = event.get("attendees", [])
            
            attendee_emails = [a.get("email", "") for a in attendees if a.get("email")]
            
            prompt = f"""
            以下の会議・イベントに関する事前ブリーフィングを日本語で作成してください。
            
            イベント: {event_title}
            説明: {event_description}
            参加者: {', '.join(attendee_emails)}
            
            以下の観点でブリーフィングを作成してください：
            1. 会議の目的・重要性
            2. 事前に準備すべき情報や資料
            3. 参加者について知っておくべき情報
            4. 会議を成功させるためのポイント
            
            簡潔で実用的な内容にしてください。
            """
            
            if self.model:
                response = self.model.generate_content(prompt)
                return response.text
            else:
                return f"イベント: {event_title}\nブリーフィングが利用できません（Gemini APIが設定されていません）"
                
        except Exception as e:
            return f"ブリーフィング生成中にエラーが発生しました: {str(e)}"