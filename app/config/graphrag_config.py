from pydantic_settings import BaseSettings
from typing import Optional


class GraphRAGConfig(BaseSettings):
    """GraphRAG配置"""

    # 数据目录
    DATA_DIR: str = "design_docs/mcp_rag_agent_graphrag_demo/doupocangqiong/output"
    # LanceDB URI
    LANCEDB_URI: str = (
        "design_docs/mcp_rag_agent_graphrag_demo/doupocangqiong/output/lancedb"
    )
    # 社区级别
    COMMUNITY_LEVEL: int = 2
    # API配置
    API_KEY: Optional[str] = None
    BASE_URL: Optional[str] = None
    MODEL: str = "qwen-turbo"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
