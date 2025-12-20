import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath('.'))

# 导入并初始化日志
from app.config.logger import logger

# 测试不同级别的日志
logger.debug("这是一条DEBUG级别的日志")
logger.info("这是一条INFO级别的日志")
logger.warning("这是一条WARNING级别的日志")
logger.error("这是一条ERROR级别的日志")
logger.critical("这是一条CRITICAL级别的日志")

print("\n日志测试完成！请检查控制台输出和logs/app.log文件。")
