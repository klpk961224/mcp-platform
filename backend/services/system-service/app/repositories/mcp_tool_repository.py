# -*- coding: utf-8 -*-
"""
MCP宸ュ叿鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. MCP宸ュ叿CRUD鎿嶄綔
2. MCP宸ュ叿查询鎿嶄綔
3. MCP宸ュ叿缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.mcp_tool_repository import MCPToolRepository
    
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
    MCP宸ュ叿鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - MCP宸ュ叿CRUD鎿嶄綔
    - MCP宸ュ叿查询鎿嶄綔
    - MCP宸ュ叿缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        tool_repo = MCPToolRepository(db)
        tool = tool_repo.get_by_code("data_analysis")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖朚CP宸ュ叿鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, tool: MCPTool) -> MCPTool:
        """
        创建MCP宸ュ叿
        
        Args:
            tool: 宸ュ叿瀵硅薄
        
        Returns:
            MCPTool: 创建鐨勫伐鍏峰璞?        """
        logger.info(f"创建MCP宸ュ叿: name={tool.name}, code={tool.code}")
        self.db.add(tool)
        self.db.commit()
        self.db.refresh(tool)
        return tool
    
    def get_by_id(self, tool_id: str) -> Optional[MCPTool]:
        """
        根据ID鑾峰彇宸ュ叿
        
        Args:
            tool_id: 宸ュ叿ID
        
        Returns:
            Optional[MCPTool]: 宸ュ叿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(MCPTool).filter(MCPTool.id == tool_id).first()
    
    def get_by_code(self, code: str) -> Optional[MCPTool]:
        """
        根据编码鑾峰彇宸ュ叿
        
        Args:
            code: 宸ュ叿编码
        
        Returns:
            Optional[MCPTool]: 宸ュ叿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(MCPTool).filter(MCPTool.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        根据租户ID鑾峰彇宸ュ叿鍒楄〃
        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[MCPTool]: 宸ュ叿鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).filter(MCPTool.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_public_tools(self, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        鑾峰彇鍏紑宸ュ叿鍒楄〃
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[MCPTool]: 宸ュ叿鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).filter(MCPTool.is_public == True).offset(offset).limit(page_size).all()
    
    def get_available_tools(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        鑾峰彇绉熸埛鍙敤鐨勫伐鍏峰垪琛紙绉熸埛绉佹湁 + 鍏紑锛?        
        Args:
            tenant_id: 租户ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[MCPTool]: 宸ュ叿鍒楄〃
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
        鎼滅储宸ュ叿
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 租户ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[MCPTool]: 宸ュ叿鍒楄〃
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
        鑾峰彇鎵€鏈夊伐鍏?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[MCPTool]: 宸ュ叿鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(MCPTool).offset(offset).limit(page_size).all()
    
    def update(self, tool: MCPTool) -> MCPTool:
        """
        更新宸ュ叿
        
        Args:
            tool: 宸ュ叿瀵硅薄
        
        Returns:
            MCPTool: 更新鍚庣殑宸ュ叿瀵硅薄
        """
        logger.info(f"更新MCP宸ュ叿: tool_id={tool.id}")
        self.db.commit()
        self.db.refresh(tool)
        return tool
    
    def delete(self, tool_id: str) -> bool:
        """
        删除宸ュ叿
        
        Args:
            tool_id: 宸ュ叿ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除MCP宸ュ叿: tool_id={tool_id}")
        tool = self.get_by_id(tool_id)
        if not tool:
            return False
        
        self.db.delete(tool)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛宸ュ叿数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 宸ュ叿数量
        """
        return self.db.query(MCPTool).filter(MCPTool.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夊伐鍏锋暟閲?        
        Returns:
            int: 宸ュ叿数量
        """
        return self.db.query(MCPTool).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€鏌ュ伐鍏风紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 宸ュ叿编码
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(MCPTool).filter(MCPTool.code == code).first() is not None
