import hmac
from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import Settings, get_settings


bearer = HTTPBearer(auto_error=False)


def create_access_token(username: str, settings: Settings) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": username, "exp": expires_at}
    return jwt.encode(payload, settings.auth_secret, algorithm="HS256")


def authenticate(username: str, password: str, settings: Settings) -> bool:
    username_matches = hmac.compare_digest(username, settings.admin_username)
    password_matches = hmac.compare_digest(password, settings.admin_password)
    return username_matches and password_matches


def require_internal_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    settings: Settings = Depends(get_settings),
) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        payload = jwt.decode(credentials.credentials, settings.auth_secret, algorithms=["HS256"])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token") from exc
    username = payload.get("sub")
    if username != settings.admin_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token")
    return username
