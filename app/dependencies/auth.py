from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.dependencies.config import get_app_settings
from app.dependencies.db import get_sqlite_db
from app.services.user_service import UserService
from app.config.logger import logger


# OAuth2密码Bearer模式
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{get_app_settings().API_V1_STR}/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_sqlite_db),
):
    """获取当前认证用户

    验证JWT令牌，获取用户信息并验证用户状态

    Args:
        token: JWT令牌
        db: 数据库会话

    Returns:
        当前认证用户对象

    Raises:
        HTTPException: 认证失败时返回401错误
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解码JWT令牌
        settings = get_app_settings()
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("JWT token missing 'sub' claim")
            raise credentials_exception
    except JWTError as e:
        logger.warning(f"JWT token decoding failed: {str(e)}")
        raise credentials_exception

    # 获取用户
    user_service = UserService()
    user = user_service.get_user_by_id(db, int(user_id))
    if user is None:
        logger.warning(f"User not found for ID: {user_id}")
        raise credentials_exception

    return user


# 认证依赖注入容器
class AuthDeps:
    """认证依赖注入容器，提供统一的认证依赖访问接口"""

    @staticmethod
    def current_user():
        """当前认证用户依赖"""
        return Depends(get_current_user)

    @staticmethod
    def oauth2():
        """OAuth2密码Bearer模式依赖"""
        return Depends(oauth2_scheme)


# 创建依赖容器实例
auth_deps = AuthDeps()
