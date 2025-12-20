from fastapi import Depends
from app.databases.base import database_manager
from app.databases.sqlite.connection import sqlite_connection

# 注册数据库连接（保持与原有代码兼容）
database_manager.register("sqlite", sqlite_connection)


# 数据库依赖注入函数
def get_sqlite_db():
    """SQLite数据库会话依赖注入

    每次请求创建新的数据库会话，请求结束后自动关闭会话
    """
    yield from sqlite_connection.get_session()


# 数据库依赖注入容器
class DatabaseDeps:
    """数据库依赖注入容器，提供统一的数据库依赖访问接口"""

    @staticmethod
    def sqlite():
        """SQLite数据库会话依赖"""
        return Depends(get_sqlite_db)


# 导出数据库连接实例
sqlite = sqlite_connection

# 创建依赖容器实例
db_deps = DatabaseDeps()
