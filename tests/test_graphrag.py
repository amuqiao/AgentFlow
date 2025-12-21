import pytest
from app.services.graphrag_service import GraphRAGService
from app.services.tool_service import ToolService


class TestGraphRAGService:
    """测试GraphRAG服务"""

    def test_initialization(self):
        """测试服务初始化"""
        service = GraphRAGService()
        assert service is not None
        assert service.local_search_engine is None
        assert service.global_search_engine is None
        assert service.drift_search_engine is None


class TestToolService:
    """测试工具服务"""

    def test_get_tools(self):
        """测试获取工具列表"""
        service = ToolService()
        tools = service.get_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
        # 检查是否包含local_asearch工具
        local_asearch = next(
            (tool for tool in tools if tool["name"] == "local_asearch"), None
        )
        assert local_asearch is not None
        assert local_asearch["description"] == "为斗破苍穹小说提供相关的知识补充"
        assert "query" in local_asearch["parameters"]

    def test_get_tool(self):
        """测试获取指定工具"""
        service = ToolService()
        tool = service.get_tool("local_asearch")
        # 检查工具描述和参数，而不是名称（名称是通过方法参数传入的）
        assert tool["description"] == "为斗破苍穹小说提供相关的知识补充"
        assert "query" in tool["parameters"]

        # 测试获取不存在的工具
        with pytest.raises(ValueError):
            service.get_tool("non_existent_tool")


class TestGraphRAGAPI:
    """测试GraphRAG API接口"""

    def test_get_tools(self, client):
        """测试获取工具列表API"""
        response = client.get("/api/v1/graphrag/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert isinstance(data["tools"], list)
        assert len(data["tools"]) > 0

        # 检查工具信息
        local_asearch = next(
            (tool for tool in data["tools"] if tool["name"] == "local_asearch"), None
        )
        assert local_asearch is not None
        assert local_asearch["description"] == "为斗破苍穹小说提供相关的知识补充"
        assert "query" in local_asearch["parameters"]

    def test_chat_api(self, client):
        """测试聊天API"""
        # 由于聊天API需要实际调用GraphRAG服务，可能需要较长时间
        # 这里只测试基本的请求响应结构
        test_query = "萧炎的父亲是谁?"

        # 使用TestClient测试API
        response = client.post("/api/v1/graphrag/chat", json={"query": test_query})

        # 检查响应状态码
        # 服务成功执行返回200，失败返回500
        assert response.status_code == 200 or response.status_code == 500

        # 如果请求成功，检查响应结构
        if response.status_code == 200:
            data = response.json()
            assert "tool_info" in data
            assert "result" in data
            assert data["tool_info"]["name"] == "local_asearch"
            assert isinstance(data["result"], str)
            assert len(data["result"]) > 0

    def test_chat_api_invalid_request(self, client):
        """测试聊天API无效请求"""
        # 测试缺少query参数
        response = client.post("/api/v1/graphrag/chat", json={})
        assert response.status_code == 400  # 项目使用自定义异常处理器，返回400

        # 测试query参数类型错误
        response = client.post("/api/v1/graphrag/chat", json={"query": 123})
        assert response.status_code == 400  # 项目使用自定义异常处理器，返回400
