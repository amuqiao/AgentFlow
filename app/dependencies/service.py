from fastapi import Depends
from app.services.user_service import UserService
from app.dependencies.db import get_sqlite_db


# 服务层依赖注入函数
def get_user_service():
    """获取用户服务实例
    
    返回单例的UserService实例，确保服务层的一致性
    """
    return UserService()


# 服务层依赖注入容器
class ServiceDeps:
    """服务层依赖注入容器，提供统一的服务层依赖访问接口"""

    @staticmethod
    def user_service():
        """用户服务依赖"""
        return Depends(get_user_service)


# 创建依赖容器实例
service_deps = ServiceDeps()
