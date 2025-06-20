#!/bin/bash

# GCPプロジェクト設定スクリプト for Janus AI Butler

# 変数設定
PROJECT_ID="janus-ai-butler-$(date +%s)"
REGION="asia-northeast1"
SERVICE_ACCOUNT_NAME="janus-backend"

echo "=== Janus AI Butler GCP Setup ==="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"

# プロジェクト作成
echo "1. Creating GCP project..."
gcloud projects create $PROJECT_ID --name="Janus AI Butler"

# プロジェクトを選択
gcloud config set project $PROJECT_ID

# 課金アカウントの設定（手動で設定が必要）
echo "2. Please set up billing for project $PROJECT_ID manually in GCP Console"
echo "   https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
echo "   Press Enter to continue after setting up billing..."
read

# 必要なAPIの有効化
echo "3. Enabling required APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable calendar-json.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable firebase.googleapis.com

# サービスアカウントの作成
echo "4. Creating service account..."
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="Janus Backend Service Account" \
    --description="Service account for Janus AI Butler backend"

# サービスアカウントに必要な権限を付与
echo "5. Granting permissions to service account..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/speech.client"

# サービスアカウントキーの作成
echo "6. Creating service account key..."
gcloud iam service-accounts keys create ../backend/gcp-service-account.json \
    --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

# Firestoreデータベースの作成
echo "7. Creating Firestore database..."
gcloud firestore databases create --region=$REGION

echo "=== Setup Complete ==="
echo "Project ID: $PROJECT_ID"
echo "Service Account: $SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"
echo "Service Account Key: ../backend/gcp-service-account.json"
echo ""
echo "Next Steps:"
echo "1. Set GOOGLE_APPLICATION_CREDENTIALS environment variable"
echo "2. Set PROJECT_ID environment variable"
echo "3. Configure Firebase Authentication in GCP Console"