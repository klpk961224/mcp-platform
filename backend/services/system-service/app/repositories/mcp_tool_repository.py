# -*- coding: utf-8 -*-
"""
MCP工具数据访问层

功能说明：
1. MCP工具CRUD操作
2. MCP工具查询操作
3. MCP工具统计操作

使用示例：
    from app.repositories.mcp_tool_repository import MCPToolRepository
    
    tool_repo = MCPToolRepository(db)
    tool = tool_repo.get_by_code("data_analysis")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.system import MCPTool


class MCPToolRepository:
    """
    MCP工具数据访问层
    
    功能：
    - MCP工具CRUD操作
    - MCP工具查询操作
    - MCP工具统计操作
    
    使用方法：
        tool_repo = MCPToolRepository(db)
        tool = tool_repo.get_by_code("data_analysis")
    """
    
    def __init__(self, db: Session):
        """
        初始化MCP工具数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, tool: MCPTool) -> MCPTool:
        """
        创建MCP工具
        
        Args:
            tool: 工具对象
        
        Returns:
            MCPTool: 创建的工具对象
        """
        logger.info(f"创建MCP工具: name={tool.name}, code={tool.code}")
        self.db.add(tool)
        self.db.commit()
        self.db.refresh(tool)
        return tool
    
    def get_by_id(self, tool_id: str) -> Optional[MCPTool]:
        """
        根据ID获取工具
        
        Args:
            tool_id: 工具ID
        
        Returns:
            Optional[MCPTool]: 工具对象，不存在返回None
        """
        return self.db.query(MCPTool).filter(MCPTool.id == tool_id).first()
    
    def get_by_code(self, code: str) -> Optional[MCPTool]:
        """
        根据编码获取工具
        
        Args:
            code: 工具编码
        
        Returns:
            Optional[MCPTool]: 工具对象，不存在返回None
        """
        return self.db.query(MCPTool).filter(MCPTool.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        根据租户ID获取工具列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[MCPTool]: 工具列表
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).filter(MCPTool.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_public_tools(self, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        获取公开工具列表
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[MCPTool]: 工具列表
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).filter(MCPTool.is_public == True).offset(offset).limit(page_size).all()
    
    def get_available_tools(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        获取租户可用的工具列表（租户私有 + 公开）
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[MCPTool]: 工具列表
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).filter(
            or_(
                MCPTool.tenant_id == tenant_id,
                MCPTool.is_public == True
            )
        ).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        搜索工具
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[MCPTool]: 工具列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(MCPTool).filter(
            or_(
                MCPTool.name.like(f"%{keyword}%"),
                MCPTool.code.like(f"%{keyword}%"),
                MCPTool.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(
                or_(
                    MCPTool.tenant_id == tenant_id,
                    MCPTool.is_public == True
                )
            )
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        获取所有工具
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[MCPTool]: 工具列表
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).offset(offset).limit(page_size).all()
    
    def update(self, tool: MCPTool) -> MCPTool:
        """
        更新工具
        
        Args:
            tool: 工具对象
        
        Returns:
            MCPTool: 更新后的工具对象
        """
        logger.info(f"更新MCP工具: tool_id={tool.id}")
        self.db.commit()
        self.db.refresh(tool)
        return tool
    
    def delete(self, tool_id: str) -> bool:
        """
        删除工具
        
        Args:
            tool_id: 工具ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除MCP工具: tool_id={tool_id}")
        tool = self.get_by_id(tool_id)
        if not tool:
            return False
        
        self.db.delete(tool)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户工具数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 工具数量
        """
        return self.db.query(MCPTool).filter(MCPTool.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        统计所有工具数量
        
        Returns:
            int: 工具数量
        """
        return self.db.query(MCPTool).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查工具编码是否存在
        
        Args:
            code: 工具编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(MCPTool).filter(MCPTool.code == code).first() is not None