from sqlalchemy.orm import Session
from typing import Optional, List
from app.repositories.base import UserRepositoryInterface
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(UserRepositoryInterface):
    """用户仓储（SQLite）"""

    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user_in: dict) -> User:
        """创建用户"""
        db_user = User(**user_in)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = self.get(user_id)
        if db_user:
            update_data = user_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> Optional[User]:
        """删除用户"""
        db_user = self.get(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
