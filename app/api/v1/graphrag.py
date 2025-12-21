from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.graphrag_service import GraphRAGService
from app.services.tool_service import ToolService

api_router = APIRouter()

# 请求模型
class ChatRequest(BaseModel):
    query: str

# 响应模型
class ToolInfo(BaseModel):
    name: str
    description: str

class ChatResponse(BaseModel):
    tool_info: ToolInfo
    result: str

class ToolParameter(BaseModel):
    type: str
    description: str

class ToolDetail(BaseModel):
    name: str
    description: str
    parameters: Dict[str, ToolParameter]

class ToolsResponse(BaseModel):
    tools: List[ToolDetail]

# 依赖注入
def get_graphrag_service():
    return GraphRAGService()

def get_tool_service():
    return ToolService()

@api_router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    graphrag_service: GraphRAGService = Depends(get_graphrag_service)
):
    """聊天接口，接受查询并返回结果"""
    try:
        result = await graphrag_service.local_search(request.query)
        return ChatResponse(
            tool_info=ToolInfo(
                name="local_asearch",
                description="为斗破苍穹小说提供相关的知识补充"
            ),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/tools", response_model=ToolsResponse)
async def get_tools(
    tool_service: ToolService = Depends(get_tool_service)
):
    """获取支持的工具列表"""
    tools_data = tool_service.get_tools()
    # 转换为ToolDetail对象列表
    tools = []
    for tool in tools_data:
        parameters = {}
        for param_name, param_info in tool["parameters"].items():
            parameters[param_name] = ToolParameter(
                type=param_info["type"],
                description=param_info["description"]
            )
        tools.append(ToolDetail(
            name=tool["name"],
            description=tool["description"],
            parameters=parameters
        ))
    return ToolsResponse(tools=tools)