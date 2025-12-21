from typing import List, Dict, Any
import os
import sys

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# 构建graphrag_server.py的完整路径
graphrag_server_path = os.path.join(project_root, 'design_docs', 'mcp_rag_agent_graphrag_demo')
# 添加到Python路径
sys.path.insert(0, graphrag_server_path)

# 打印路径信息，用于调试
print(f"Project root: {project_root}")
print(f"GraphRAG server path: {graphrag_server_path}")
print(f"Python path: {sys.path[:3]}")

# 从graphrag_server.py导入核心功能
try:
    from graphrag_server import (
        build_local_search_engine,
        build_global_search_engine,
        build_drift_search_engine
    )
    print("Successfully imported from graphrag_server")
except ModuleNotFoundError as e:
    print(f"Error importing from graphrag_server: {e}")
    # 尝试另一种导入方式
    import importlib.util
    spec = importlib.util.spec_from_file_location("graphrag_server", os.path.join(graphrag_server_path, "graphrag_server.py"))
    graphrag_server = importlib.util.module_from_spec(spec)
    sys.modules["graphrag_server"] = graphrag_server
    spec.loader.exec_module(graphrag_server)
    
    # 从动态导入的模块中获取函数
    build_local_search_engine = graphrag_server.build_local_search_engine
    build_global_search_engine = graphrag_server.build_global_search_engine
    build_drift_search_engine = graphrag_server.build_drift_search_engine
    print("Successfully imported using dynamic import")

class GraphRAGService:
    """GraphRAG服务类，封装核心搜索功能"""
    
    def __init__(self):
        """初始化GraphRAG服务"""
        self.local_search_engine = None
        self.global_search_engine = None
        self.drift_search_engine = None
    
    async def local_search(self, query: str) -> str:
        """本地搜索接口"""
        if not self.local_search_engine:
            self.local_search_engine = build_local_search_engine()
        result = await self.local_search_engine.asearch(query)
        return result.response
    
    async def global_search(self, query: str) -> str:
        """全局搜索接口"""
        if not self.global_search_engine:
            self.global_search_engine = build_global_search_engine()
        result = await self.global_search_engine.asearch(query)
        return result.response
    
    async def drift_search(self, query: str) -> str:
        """DRIFT搜索接口"""
        if not self.drift_search_engine:
            self.drift_search_engine = build_drift_search_engine()
        result = await self.drift_search_engine.asearch(query)
        return result.response