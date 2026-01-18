# -*- coding: utf-8 -*-
"""
MCP工具服务

功能说明：
1. MCP工具管理
2. MCP工具调用
3. MCP工具监控

使用示例：
    from app.services.mcp_tool_service import MCPToolService
    
    tool_service = MCPToolService(db)
    tool = tool_service.create_tool(name="数据分析", code="data_analysis")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
import httpx
from datetime import datetime

from common.database.models.system import MCPTool
from app.repositories.mcp_tool_repository import MCPToolRepository


class MCPToolService:
    """
    MCP工具服务
    
    功能：
    - MCP工具管理
    - MCP工具调用
    - MCP工具监控
    
    使用方法：
        tool_service = MCPToolService(db)
        tool = tool_service.create_tool(name="数据分析", code="data_analysis")
    """
    
    def __init__(self, db: Session):
        """
        初始化MCP工具服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.tool_repo = MCPToolRepository(db)
    
    def create_tool(self, tool_data: Dict[str, Any]) -> MCPTool:
        """
        创建MCP工具
        
        Args:
            tool_data: 工具数据
        
        Returns:
            MCPTool: 创建的工具对象
        
        Raises:
            ValueError: 工具编码已存在
        """
        logger.info(f"创建MCP工具: name={tool_data.get('name')}, code={tool_data.get('code')}")
        
        # 检查工具编码是否已存在
        if self.tool_repo.exists_by_code(tool_data.get("code")):
            raise ValueError("工具编码已存在")
        
        # 创建工具
        tool = MCPTool(**tool_data)
        return self.tool_repo.create(tool)
    
    def get_tool(self, tool_id: str) -> Optional[MCPTool]:
        """
        获取工具
        
        Args:
            tool_id: 工具ID
        
        Returns:
            Optional[MCPTool]: 工具对象，不存在返回None
        """
        return self.tool_repo.get_by_id(tool_id)
    
    def get_tool_by_code(self, code: str) -> Optional[MCPTool]:
        """
        根据编码获取工具
        
        Args:
            code: 工具编码
        
        Returns:
            Optional[MCPTool]: 工具对象，不存在返回None
        """
        return self.tool_repo.get_by_code(code)
    
    def update_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> Optional[MCPTool]:
        """
        更新工具
        
        Args:
            tool_id: 工具ID
            tool_data: 工具数据
        
        Returns:
            Optional[MCPTool]: 更新后的工具对象，不存在返回None
        """
        logger.info(f"更新MCP工具: tool_id={tool_id}")
        
        tool = self.tool_repo.get_by_id(tool_id)
        if not tool:
            return None
        
        # 更新工具
        for key, value in tool_data.items():
            if hasattr(tool, key):
                setattr(tool, key, value)
        
        return self.tool_repo.update(tool)
    
    def delete_tool(self, tool_id: str) -> bool:
        """
        删除工具
        
        Args:
            tool_id: 工具ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除MCP工具: tool_id={tool_id}")
        return self.tool_repo.delete(tool_id)
    
    def list_tools(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                   status: Optional[str] = None, is_public: Optional[bool] = None,
                   page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        获取工具列表
        
        Args:
            tenant_id: 租户ID（可选）
            keyword: 搜索关键词（可选）
            status: 状态（可选）
            is_public: 是否公开（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[MCPTool]: 工具列表
        """
        if keyword:
            return self.tool_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.tool_repo.get_available_tools(tenant_id, page, page_size)
        else:
            return self.tool_repo.get_all(page, page_size)
    
    async def execute_tool(self, tool_id: str, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        执行MCP工具
        
        Args:
            tool_id: 工具ID
            params: 参数
            user_id: 用户ID
        
        Returns:
            Dict[str, Any]: 执行结果
        
        Raises:
            ValueError: 工具不存在或不可用
            ValueError: 参数验证失败
        """
        logger.info(f"执行MCP工具: tool_id={tool_id}, user_id={user_id}")
        
        # 获取工具
        tool = self.tool_repo.get_by_id(tool_id)
        if not tool:
            raise ValueError("工具不存在")
        
        if not tool.is_available():
            raise ValueError("工具不可用")
        
        # 执行工具
        result = await self._execute_http_request(tool, params)
        
        # 更新统计信息
        tool.increment_call_count(success=True)
        self.tool_repo.update(tool)
        
        return result
    
    async def _execute_http_request(self, tool: MCPTool, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行HTTP请求
        
        Args:
            tool: 工具对象
            params: 参数
        
        Returns:
            Dict[str, Any]: 执行结果
        """
        timeout = tool.api_timeout
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                if tool.api_method.upper() == "GET":
                    response = await client.get(tool.api_endpoint, params=params)
                elif tool.api_method.upper() == "POST":
                    response = await client.post(tool.api_endpoint, json=params)
                elif tool.api_method.upper() == "PUT":
                    response = await client.put(tool.api_endpoint, json=params)
                elif tool.api_method.upper() == "DELETE":
                    response = await client.delete(tool.api_endpoint, json=params)
                else:
                    raise ValueError(f"不支持的HTTP方法: {tool.api_method}")
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPError as e:
                logger.error(f"HTTP请求失败: {e}")
                raise ValueError(f"HTTP请求失败: {str(e)}")
    
    def get_tool_statistics(self, tool_id: str) -> Dict[str, Any]:
        """
        获取工具统计信息
        
        Args:
            tool_id: 工具ID
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        tool = self.tool_repo.get_by_id(tool_id)
        if not tool:
            return {}
        
        return {
            "tool_id": tool.id,
            "name": tool.name,
            "call_count": tool.call_count,
            "success_count": tool.success_count,
            "fail_count": tool.fail_count,
            "success_rate": tool.get_success_rate(),
            "last_called_at": tool.last_called_at.isoformat() if tool.last_called_at else None,
        }
    
    def count_tools(self, tenant_id: Optional[str] = None) -> int:
        """
        统计工具数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 工具数量
        """
        if tenant_id:
            return self.tool_repo.count_by_tenant(tenant_id)
        else:
            return self.tool_repo.count_all()