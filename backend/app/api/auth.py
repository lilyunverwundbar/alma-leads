from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import authenticate, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, settings: Settings = Depends(get_settings)) -> TokenResponse:
    if not authenticate(payload.username, payload.password, settings):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(payload.username, settings))
