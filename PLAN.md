# 開発計画

## セッション1: 基盤構築とバックエンド開発開始

### 目標
双貌のAI執事 "Janus" の開発を開始し、基盤となるバックエンドシステムを構築する

### 実施内容
1. **プロジェクト基盤の構築**
   - GCP設定自動化スクリプト作成 (`scripts/setup_gcp.sh`)
   - 必要なAPIの有効化コマンド（Vertex AI、Cloud Run、Speech-to-Text、Calendar API、Firestore）
   - サービスアカウント作成とIAM権限設定
   - 課金設定ガイドラインの追加

2. **バックエンド開発環境の構築**
   - ディレクトリ構造の作成（backend/api/, backend/services/, flutter_app/lib/）
   - FastAPI依存関係定義 (`backend/requirements.txt`)
   - beautifulsoup4, httpx, google-cloud-* パッケージ追加
   - プロジェクト初期化ファイル作成

3. **API基盤の実装**
   - FastAPIメインアプリケーション (`backend/api/main.py`)
     - CORS設定、ルーター統合、ヘルスチェックエンドポイント
   - Firebase認証システム (`backend/api/auth.py`)
     - JWT トークン検証、ユーザー情報取得
   - Past-Mode API (`backend/api/past_mode.py`)
     - コンテンツキャプチャ、ダイジェスト取得、バッチ処理エンドポイント
   - Future-Mode API (`backend/api/future_mode.py`)
     - 予定取得、ブリーフィング生成、通知管理

4. **サービスレイヤー実装**
   - Gemini AI連携 (`backend/services/gemini_service.py`)
     - URL要約機能（BeautifulSoup使用）、テキスト要約、ブリーフィング生成
   - Firestore連携 (`backend/services/firestore_service.py`)
     - キャプチャ保存、処理済みデータ取得、バッチ処理対応
   - Google Calendar連携 (`backend/services/calendar_service.py`)
     - 予定取得、重要イベント判定、ブリーフィング対象選別

### 実際の成果物
- `scripts/setup_gcp.sh` - GCP環境自動セットアップ（実行権限付与済み）
- `backend/api/main.py` - FastAPIメインアプリケーション
- `backend/api/auth.py` - Firebase認証システム
- `backend/api/past_mode.py` - Past-Mode API（3エンドポイント）
- `backend/api/future_mode.py` - Future-Mode API（3エンドポイント）
- `backend/services/gemini_service.py` - Gemini AI連携サービス
- `backend/services/firestore_service.py` - Firestore連携サービス
- `backend/services/calendar_service.py` - Google Calendar連携サービス
- `backend/requirements.txt` - Python依存関係（14パッケージ）
- ディレクトリ構造完成（backend/, flutter_app/, scripts/）

### 技術的詳細
**実装済みAPI エンドポイント:**
- `GET /` - ルートエンドポイント
- `GET /health` - ヘルスチェック
- `POST /auth/verify` - Firebase認証トークン検証
- `POST /past/capture` - コンテンツキャプチャ（URL/テキスト/音声）
- `GET /past/digest` - 朝のダイジェスト取得
- `POST /past/process-batch` - 夜間バッチ処理
- `GET /future/upcoming-events` - 今後の予定取得
- `POST /future/generate-briefing` - ブリーフィング生成
- `GET /future/briefings` - ブリーフィング一覧取得

**主要機能:**
- Firebase Authentication統合
- Vertex AI Gemini 1.5 Pro統合
- Google Calendar API統合
- Firestore NoSQLデータベース統合
- 非同期処理対応（async/await）
- CORS設定済みAPI
- エラーハンドリング実装

---

## セッション2: 環境設定とテスト実装

### 目標
セッション1で構築したバックエンドシステムの環境設定を行い、実際にAPIサーバーを起動してテストを実施する

### 実施内容
1. **開発環境のセットアップ**
   - Python仮想環境の作成
   - 依存関係パッケージのインストール
   - 環境変数の設定

2. **APIサーバーの起動とテスト**
   - FastAPIサーバーのローカル起動
   - ヘルスチェックエンドポイントの確認
   - Swagger UIでのAPI仕様確認

3. **コード修正と調整**
   - インポートエラーの修正
   - 非同期処理の調整
   - エラーハンドリングの改善

4. **基本機能のテスト**
   - Past-Mode API の動作確認
   - Future-Mode API の動作確認
   - 認証システムの動作確認

### 実際の成果物
- Python 3.11仮想環境の作成完了
- 全依存関係パッケージのインストール成功（14パッケージ）
- FastAPIサーバーの起動確認完了
- インポートエラーの修正完了
- 簡易版テストサーバー（`test_main.py`）作成
- API基本構造の動作確認完了

### 技術的解決事項
- **Python 3.13互換性問題**: Python 3.11への変更で解決
- **相対インポートエラー**: 絶対インポートに変更
- **Vertex AI依存問題**: テスト用の簡易版APIで回避
- **パッケージビルドエラー**: pydantic-coreコンパイル問題をPython 3.11で解決

### 動作確認済み機能
- FastAPIアプリケーションの起動
- CORS設定の有効化
- ヘルスチェックエンドポイント（`/health`）
- ルートエンドポイント（`/`）
- テスト用キャプチャエンドポイント（`/test/capture`）

---

## セッション3: Webプロトタイプ開発

### 目標
Flutterがインストールされていないため、代替案としてWebプロトタイプ版からJanusアプリケーションの開発を開始する

### 実施内容
1. **環境確認と代替案の策定**
   - Flutter環境の確認（インストールされていないことを確認）
   - Webプロトタイプによる開発方針の決定
   - バックエンドAPIの動作確認

2. **Webプロトタイプの開発**
   - HTML/CSS/JavaScriptによるWebアプリケーション作成
   - Past-Mode（記録官）とFuture-Mode（機会発見官）の双貌UI実装
   - レスポンシブデザインの適用
   - モダンなUIデザイン（グラデーション、カード型レイアウト）

3. **API連携の実装**
   - バックエンドAPIとの通信機能
   - エラーハンドリングとローディング表示
   - モックデータによる動作確認

4. **テストと動作確認**
   - Webサーバーの起動確認
   - API通信テスト
   - 各機能の動作確認

### 実際の成果物
- `web_prototype/index.html` - メインHTMLファイル（Past/Future Mode切り替え）
- `web_prototype/styles.css` - モダンなUIスタイル（299行）
- `web_prototype/app.js` - JavaScript アプリケーションロジック（262行）
- `web_prototype/README.md` - セットアップ手順とテスト結果

### 技術的詳細
**実装済みWebアプリ機能:**
- 🎭 双貌UI（Past Mode ⇔ Future Mode切り替え）
- 📚 Past Mode機能:
  - コンテンツキャプチャ（URL/テキスト/音声）
  - 朝のダイジェスト表示
  - APIとの連携テスト
- 🔮 Future Mode機能:
  - 今後の予定表示（モック）
  - ブリーフィング生成（モック）
  - カレンダー連携準備
- 🎨 UI/UX機能:
  - レスポンシブデザイン
  - グラデーション背景
  - カード型レイアウト
  - ローディングアニメーション
  - トースト通知

**動作確認済み:**
- バックエンドAPI（http://127.0.0.1:8000）との通信
- Webサーバー（http://localhost:3000）での動作
- コンテンツキャプチャ機能のテスト
- エラーハンドリングと通知機能

### 次回セッション予定
**セッション4: 実際のAI機能統合**
- Gemini API連携の実装
- Google Calendar API連携
- Firebase認証の統合
- 実際のデータ処理パイプライン構築