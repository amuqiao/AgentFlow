from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.dependencies.config import app_settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """生成访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """解码访问令牌"""
    try:
        payload = jwt.decode(token, app_settings.SECRET_KEY, algorithms=[app_settings.ALGORITHM])
        return payload
    except JWTError:
        return None
