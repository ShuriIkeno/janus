# Janus Web Prototype

双貌のAI執事 "Janus" のWebプロトタイプ版です。

## セットアップ手順

### 1. バックエンドAPIサーバーの起動

```bash
cd backend
source ../venv/bin/activate
python -m uvicorn test_main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Webサーバーの起動

```bash
cd web_prototype
python -m http.server 3000
```

### 3. アクセス

ブラウザで以下のURLにアクセス:
- Webアプリ: http://localhost:3000
- API Swagger UI: http://127.0.0.1:8000/docs

## 機能

### Past Mode (記録官 - The Archivist)
- **好奇心のキャプチャ**: URL、テキスト、音声メモを保存
- **朝のダイジェスト**: キャプチャした情報の要約表示

### Future Mode (機会発見官 - The Pathfinder)  
- **今後の予定**: Google Calendarとの連携（モック版）
- **ブリーフィング**: 会議等の事前準備情報生成

## テスト済み機能

- ✅ Mode切り替え (Past ⇔ Future)
- ✅ APIサーバーとの通信
- ✅ コンテンツキャプチャ機能
- ✅ レスポンシブデザイン
- ✅ エラーハンドリング
- ✅ ローディング表示

## 今後の開発

- [ ] 実際のGemini API連携
- [ ] Google Calendar API連携  
- [ ] Firebase認証
- [ ] Firestore連携
- [ ] プッシュ通知
- [ ] Flutter版への移行