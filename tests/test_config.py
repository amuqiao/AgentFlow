from fastapi.testclient import TestClient
from main import app
from app.dependencies.config import app_settings, sqlite_config, logging_config
from app.dependencies.config import BaseSettings
import logging


def test_config_loading():
    """测试配置加载功能"""
    # 测试应用配置
    assert app_settings.APP_NAME == "AgentFlow"
    assert app_settings.ENVIRONMENT == "development"
    assert app_settings.DEBUG is True

    # 测试数据库配置
    assert sqlite_config.DATABASE == "agentflow"
    assert sqlite_config.DATABASE_FILE == "app.db"
    assert sqlite_config.URL == "sqlite:///app.db"

    # 测试日志配置
    assert logging_config.LEVEL == "INFO"
    assert logging_config.FILE == "logs/app.log"
    assert logging_config.MAX_BYTES == 10 * 1024 * 1024
    assert logging_config.BACKUP_COUNT == 5


def test_config_from_env():
    """测试从指定环境文件加载配置"""

    # 创建一个简单的测试配置类
    class TestConfig(BaseSettings):
        TEST_KEY: str = "default_value"

        model_config = BaseSettings.model_config.copy()
        model_config["env_prefix"] = "TEST_"

    # 测试默认配置
    default_config = TestConfig()
    assert default_config.TEST_KEY == "default_value"

    # 测试通过环境变量覆盖配置
    import os

    os.environ["TEST_TEST_KEY"] = "env_value"
    env_config = TestConfig()
    assert env_config.TEST_KEY == "env_value"
    # 清理环境变量
    del os.environ["TEST_TEST_KEY"]


def test_config_dependency_injection():
    """测试配置依赖注入"""
    client = TestClient(app)

    # 测试配置注入是否正常工作
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    config_data = response.json()
    assert "app_name" in config_data
    assert "environment" in config_data
    assert "sqlite_url" in config_data
    assert config_data["app_name"] == app_settings.APP_NAME


def test_logging_config():
    """测试日志配置"""
    # 测试日志模块配置
    from app.config.logger import logger

    # 测试日志级别设置
    assert logger.level == logging.INFO

    # 测试日志记录功能
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # 测试日志文件是否创建
    import os

    if logging_config.FILE:
        assert os.path.exists(logging_config.FILE)
