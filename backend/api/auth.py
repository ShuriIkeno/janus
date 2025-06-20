from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth, credentials
import os

auth_router = APIRouter()
security = HTTPBearer()

# Firebase Admin SDK初期化
if not firebase_admin._apps:
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

class UserResponse(BaseModel):
    uid: str
    email: str
    name: str

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@auth_router.post("/verify", response_model=UserResponse)
async def verify_token(user = Depends(get_current_user)):
    return UserResponse(
        uid=user["uid"],
        email=user.get("email", ""),
        name=user.get("name", "")
    )