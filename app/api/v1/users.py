from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import db_deps, auth_deps, service_deps
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = auth_deps.current_user()):
    """获取当前用户信息"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = db_deps.sqlite(),
    current_user: User = auth_deps.current_user(),
    user_service=service_deps.user_service(),
):
    """根据ID获取用户信息"""
    # 这里可以添加权限检查，比如只有管理员可以查看其他用户信息
    return user_service.get_user_by_id(db, user_id)
