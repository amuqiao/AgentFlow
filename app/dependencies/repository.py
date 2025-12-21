from fastapi import Depends
from app.dependencies.db import get_sqlite_db
from app.repositories.sqlite.user_repository import UserRepository
from app.repositories.base import UserRepositoryInterface


# 仓储层依赖注入函数
def get_user_repository(db=Depends(get_sqlite_db)):
    """获取用户仓储实例
    
    返回UserRepository实例，实现UserRepositoryInterface接口
    """
    return UserRepository(db)


# 仓储层依赖注入容器
class RepositoryDeps:
    """仓储层依赖注入容器，提供统一的仓储层依赖访问接口"""
    
    @staticmethod
    def user_repository():
        """用户仓储依赖"""
        return Depends(get_user_repository)


# 创建依赖容器实例
repository_deps = RepositoryDeps()
