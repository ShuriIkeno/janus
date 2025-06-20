# CLAUDE.md - AI執事 "Janus" 開発ガイド

## プロジェクト概要

### プロジェクト名
**双貌のAI執事 "Janus" (ヤヌス)**

### コンセプト
ユーザーの「過去の忘れられた好奇心」と「未来の見過ごされる機会」という、時間軸の異なる2つの課題を同時に解決する、双貌のAI執事。

### ペルソナ
- **名前**: 田中 健太 (29歳)
- **職業**: UI/UXデザイナー
- **課題**:
  - 過去への課題: 日々の情報洪水の中で、せっかく抱いた知的好奇心を忘れてしまい、知識が断片化している
  - 未来への課題: 目前のタスクに追われ、少し先にあるビジネスチャンスや、人生を豊かにする新しい出会いを見過ごしている

## システムアーキテクチャ

### 技術スタック
- **フロントエンド**: Flutter（iOS/Android/Web対応）
- **バックエンド**: Python (FastAPI or Flask)
- **AI/ML**: 
  - Vertex AI - Gemini 1.5 Pro
  - Vertex AI Agent Builder
- **データベース**: Firestore
- **インフラ**: 
  - Cloud Run（バックエンドAPI）
  - Firebase（認証、プッシュ通知）
- **API連携**:
  - Google Calendar API
  - Speech-to-Text API
  - Web Search API

## 機能要件

### C-01: ユーザー認証
- Googleアカウントでのサインイン/サインアップ
- データのユーザーごとの隔離

### Past-Mode: 記録官 (The Archivist)

#### P-01: 好奇心のキャプチャ
- P-01-a: WebページのURL保存
- P-01-b: テキスト断片の保存
- P-01-c: 音声メモの保存

#### P-02: 夜間バッチ処理
- P-02-a: URLやテキストをGemini APIで要約生成
- P-02-b: 音声メモをSpeech-to-Text APIでテキスト化し、Gemini APIで解釈・要約

#### P-03: 朝のダイジェスト表示
- P-03-a: タイトル、要約、サムネイルでの分かりやすい表示
- P-03-b: 元の情報ソースへのリンク

### Future-Mode: 機会発見官 (The Pathfinder)

#### F-01: 未来の文脈の参照
- F-01-a: Google Calendar APIとの連携（会議、出張などの予定取得）

#### F-02: 事前ブリーフィングの生成
- F-02-a: 会議参加者や議題に基づく関連情報の収集・要約

#### F-03: ジャストインタイム通知
- F-03-a: 予定の24時間前などにプッシュ通知送信

## MVP実装スコープ

### フェーズ1: 基盤構築
1. GCPプロジェクト作成と設定
2. 必要なAPIの有効化
3. Gemini API接続テスト

### フェーズ2: Past-Mode最小実装
1. WebフォームでのURL入力機能
2. Gemini APIを使った要約生成
3. Firestoreへの保存
4. 要約結果の一覧表示

### フェーズ3: Future-Mode最小実装
1. Google Calendar API連携
2. 予定に基づくブリーフィング生成
3. 結果の表示

### フェーズ4: 統合とUI実装
1. Flutterでのモバイルアプリ開発
2. 朝のダイジェスト画面のデザイン実装
3. プッシュ通知の実装（または演出）

## ディレクトリ構成案
```
janus/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI メインアプリケーション
│   │   ├── auth.py            # 認証関連
│   │   ├── past_mode.py       # Past-Mode エンドポイント
│   │   └── future_mode.py     # Future-Mode エンドポイント
│   ├── services/
│   │   ├── gemini_service.py  # Gemini API 連携
│   │   ├── calendar_service.py # Google Calendar 連携
│   │   └── firestore_service.py
│   └── requirements.txt
├── flutter_app/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   │   ├── login_screen.dart
│   │   │   ├── home_screen.dart
│   │   │   ├── digest_screen.dart
│   │   │   └── capture_screen.dart
│   │   ├── services/
│   │   │   └── api_service.dart
│   │   └── widgets/
│   └── pubspec.yaml
├── scripts/
│   └── setup_gcp.sh
└── README.md
```

## 開発の進め方

### ステップ1: 環境構築
```bash
# GCPプロジェクトの作成
gcloud projects create janus-ai-butler-[unique-id]

# 必要なAPIの有効化
gcloud services enable vertexai.googleapis.com
gcloud services enable cloudrun.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable calendar-json.googleapis.com

# サービスアカウントの作成
gcloud iam service-accounts create janus-backend
```

### ステップ2: バックエンド開発
```python
# backend/api/main.py の基本構造
from fastapi import FastAPI
from .auth import auth_router
from .past_mode import past_router
from .future_mode import future_router

app = FastAPI(title="Janus AI Butler API")

app.include_router(auth_router, prefix="/auth")
app.include_router(past_router, prefix="/past")
app.include_router(future_router, prefix="/future")
```

### ステップ3: Flutter開発
```dart
// flutter_app/lib/main.dart の基本構造
import 'package:flutter/material.dart';

void main() {
  runApp(JanusApp());
}

class JanusApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Janus AI Butler',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginScreen(),
    );
  }
}
```

## 重要な実装ポイント

### 1. 非同期処理の実装
Past-Modeの夜間バッチ処理は、Cloud SchedulerとCloud Functionsを組み合わせて実装

### 2. セキュリティ
- Firebase Authenticationを使用したユーザー認証
- APIエンドポイントの適切な認証・認可

### 3. UX設計
- 「朝のダイジェスト」は雑誌のような美しいレイアウト
- 情報のキャプチャは最小限のアクション（ワンタップ/ワンキー）

### 4. データ設計
```javascript
// Firestore のデータ構造例
users/
  {userId}/
    profile: { name, email, preferences }
    captures/
      {captureId}: {
        type: "url" | "text" | "voice",
        content: "...",
        timestamp: "...",
        processed: false,
        summary: "..." // 処理後に追加
      }
    briefings/
      {briefingId}: {
        eventId: "...", // Calendar event ID
        eventTitle: "...",
        eventTime: "...",
        briefingContent: "...",
        createdAt: "..."
      }
```

## デモ動画のポイント

1. **オープニング（30秒）**
   - 健太の課題を視覚的に表現（情報の洪水、忘れられる好奇心）

2. **Past-Mode実演（1分）**
   - 日中：気になった情報を簡単にキャプチャ
   - 翌朝：美しいダイジェストを見て驚く様子

3. **Future-Mode実演（1分）**
   - カレンダーに予定が入る
   - 適切なタイミングでブリーフィング通知
   - 会議で活用される様子

4. **クロージング（30秒）**
   - PastとFutureの連携による価値の説明

## 注意事項

- **プライバシー**: カレンダー情報などの取り扱いには最大限の注意を払う
- **パフォーマンス**: Gemini APIの呼び出し回数とコストに注意
- **スケーラビリティ**: MVP段階では考慮しないが、将来的な拡張性は意識する

## 追加アイデア（将来的な拡張）

- 音声での情報キャプチャ（ボイスメモ）
- ブラウザ拡張機能での自動キャプチャ
- Slack、Jira、Google Driveなどとの連携
- 興味プロファイルの自動学習とパーソナライゼーション
- 位置情報を活用したセレンディピティの演出