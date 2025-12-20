from app.databases.base import database_manager
from app.databases.sqlite.connection import sqlite_connection

# 注册数据库连接
database_manager.register("sqlite", sqlite_connection)

# 导出数据库连接实例
sqlite = sqlite_connection

# 导出数据库管理器
__all__ = [
    "database_manager",
    "sqlite",
]
