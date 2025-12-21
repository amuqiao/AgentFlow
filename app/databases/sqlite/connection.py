from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config.database import sqlite_config
from app.databases.base import DatabaseConnection
from app.config.logger import logger
from app.models.base import Base


class SQLiteConnection(DatabaseConnection):
    """SQLite数据库连接管理"""

    def __init__(self):
        self._engine = None
        self._SessionLocal = None
        self._Base = Base

    def connect(self):
        """建立SQLite连接"""
        try:
            self._engine = create_engine(
                sqlite_config.URL,
                connect_args={
                    "check_same_thread": False
                },  # SQLite特定配置，允许在多线程中使用
            )
            self._SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self._engine
            )
            # 测试连接
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("SQLite连接成功")
        except Exception as e:
            logger.error(f"SQLite连接失败: {str(e)}")
            raise

    def disconnect(self):
        """断开SQLite连接"""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            logger.info("SQLite连接已断开")

    def get_session(self):
        """获取SQLite会话"""
        if not self._SessionLocal:
            self.connect()
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @property
    def engine(self):
        """获取SQLite引擎"""
        if not self._engine:
            self.connect()
        return self._engine

    @property
    def Base(self):
        """获取SQLite模型基类"""
        return self._Base


# SQLite连接实例
sqlite_connection = SQLiteConnection()
