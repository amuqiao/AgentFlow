from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import db_deps, service_deps, config_deps
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(
    user_create: UserCreate,
    db: Session = db_deps.sqlite(),
    user_service=service_deps.user_service(),
):
    """用户注册"""
    user = user_service.register_user(db, user_create)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = db_deps.sqlite(),
    user_service=service_deps.user_service(),
    app_settings=config_deps.app(),
):
    """用户登录"""
    # 验证用户
    user = user_service.authenticate_user(db, form_data.username, form_data.password)

    # 生成访问令牌
    access_token = user_service.generate_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": app_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
