from typing import List, Dict, Any


class ToolService:
    """工具服务类，管理支持的工具"""

    def __init__(self):
        """初始化工具服务"""
        self.tools = {
            "local_asearch": {
                "description": "为斗破苍穹小说提供相关的知识补充",
                "parameters": {
                    "query": {"type": "string", "description": "查询字符串"}
                },
            }
        }

    def get_tools(self) -> List[Dict[str, Any]]:
        """获取所有支持的工具"""
        tool_list = []
        for tool_name, tool_info in self.tools.items():
            tool_list.append(
                {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"],
                }
            )
        return tool_list

    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """获取指定工具的信息"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        return self.tools[tool_name]
