from app.config.base import BaseSettings
from typing import Optional, Dict, Any
import logging
import json
from datetime import datetime


class LoggingConfig(BaseSettings):
    """日志配置"""

    # 日志级别配置
    LEVEL: str = "INFO"  # 主日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL

    # 日志文件配置
    FILE: Optional[str] = "logs/app.log"  # 日志文件路径，None表示不输出到文件
    MAX_BYTES: int = 10 * 1024 * 1024  # 单个日志文件最大字节数(10MB)
    BACKUP_COUNT: int = 5  # 保留的日志文件数量

    # 日志格式配置
    FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # 控制台日志配置
    CONSOLE_LEVEL: Optional[str] = None  # 控制台日志级别，None表示与主级别相同

    # 文件日志配置
    FILE_LEVEL: Optional[str] = None  # 文件日志级别，None表示与主级别相同

    # 日志模块级别配置 - 可以为不同模块设置不同日志级别
    MODULE_LEVELS: Dict[str, str] = {
        "uvicorn": "INFO",
        "fastapi": "INFO",
        "sqlalchemy": "WARNING",
        "app": "INFO",
    }

    # 是否禁用默认日志配置
    DISABLE_DEFAULT_LOGGERS: bool = False

    model_config = BaseSettings.model_config.copy()
    model_config["env_prefix"] = "LOGGING_"


# 创建日志配置实例
logging_config = LoggingConfig()


# 使用默认的日志格式化器，确保中文正常显示
class EnhancedFormatter(logging.Formatter):
    """增强型日志格式化器，支持自定义格式和异常信息"""
    
    def format(self, record):
        # 添加请求相关信息到record
        record.request_id = getattr(record, "request_id", "")
        record.path = getattr(record, "path", "")
        record.method = getattr(record, "method", "")
        record.client_ip = getattr(record, "client_ip", "")
        record.code = getattr(record, "code", 0)
        
        # 使用配置的日志格式
        return super().format(record)


# 配置日志器
logger = logging.getLogger("app")
logger.setLevel(getattr(logging, logging_config.LEVEL))
logger.propagate = False  # 避免日志重复传递到根日志器

# 移除默认处理器
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 创建增强型日志格式化器，支持更多字段
log_format = logging_config.FORMAT
if "%(request_id)s" not in log_format:
    log_format += " - RequestID: %(request_id)s - Path: %(path)s - Method: %(method)s - ClientIP: %(client_ip)s - Code: %(code)s"

formatter = EnhancedFormatter(
    fmt=log_format,
    datefmt=logging_config.DATE_FORMAT
)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
# 设置控制台日志级别
if logging_config.CONSOLE_LEVEL:
    console_handler.setLevel(getattr(logging, logging_config.CONSOLE_LEVEL))
else:
    console_handler.setLevel(getattr(logging, logging_config.LEVEL))
logger.addHandler(console_handler)

# 添加文件处理器（如果配置了文件路径）
if logging_config.FILE:
    import os
    from logging.handlers import RotatingFileHandler
    
    # 创建日志目录
    log_dir = os.path.dirname(logging_config.FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 创建带编码的文件处理器，确保中文正常显示
    file_handler = RotatingFileHandler(
        logging_config.FILE,
        maxBytes=logging_config.MAX_BYTES,
        backupCount=logging_config.BACKUP_COUNT,
        encoding='utf-8'  # 确保中文正常显示
    )
    file_handler.setFormatter(formatter)
    # 设置文件日志级别
    if logging_config.FILE_LEVEL:
        file_handler.setLevel(getattr(logging, logging_config.FILE_LEVEL))
    else:
        file_handler.setLevel(getattr(logging, logging_config.LEVEL))
    logger.addHandler(file_handler)

# 配置其他模块的日志级别
for module_name, level in logging_config.MODULE_LEVELS.items():
    module_logger = logging.getLogger(module_name)
    module_logger.setLevel(getattr(logging, level))
    # 确保子模块日志不会重复
    module_logger.propagate = False
