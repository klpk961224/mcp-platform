# -*- coding: utf-8 -*-
"""
岗位服务

功能说明：
1. 岗位CRUD操作
2. 岗位查询操作
3. 岗位统计操作

使用示例：
    from app.services.position_service import PositionService
    
    position_service = PositionService(db)
    position = position_service.create_position(name="开发工程师", code="developer")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.position import Position
from app.repositories.position_repository import PositionRepository


class PositionService:
    """
    岗位服务
    
    功能：
    - 岗位CRUD操作
    - 岗位查询操作
    - 岗位统计操作
    
    使用方法：
        position_service = PositionService(db)
        position = position_service.create_position(name="开发工程师", code="developer")
    """
    
    def __init__(self, db: Session):
        """
        初始化岗位服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.position_repo = PositionRepository(db)
    
    def create_position(self, position_data: Dict[str, Any]) -> Position:
        """
        创建岗位
        
        Args:
            position_data: 岗位数据
        
        Returns:
            Position: 创建的岗位对象
        
        Raises:
            ValueError: 岗位编码已存在
        """
        logger.info(f"创建岗位: name={position_data.get('name')}, code={position_data.get('code')}")
        
        # 检查岗位编码是否已存在
        if self.position_repo.exists_by_code(position_data.get("code")):
            raise ValueError("岗位编码已存在")
        
        # 创建岗位
        position = Position(**position_data)
        return self.position_repo.create(position)
    
    def get_position(self, position_id: str) -> Optional[Position]:
        """
        获取岗位
        
        Args:
            position_id: 岗位ID
        
        Returns:
            Optional[Position]: 岗位对象，不存在返回None
        """
        return self.position_repo.get_by_id(position_id)
    
    def get_position_by_code(self, code: str) -> Optional[Position]:
        """
        根据编码获取岗位
        
        Args:
            code: 岗位编码
        
        Returns:
            Optional[Position]: 岗位对象，不存在返回None
        """
        return self.position_repo.get_by_code(code)
    
    def update_position(self, position_id: str, position_data: Dict[str, Any]) -> Optional[Position]:
        """
        更新岗位
        
        Args:
            position_id: 岗位ID
            position_data: 岗位数据
        
        Returns:
            Optional[Position]: 更新后的岗位对象，不存在返回None
        """
        logger.info(f"更新岗位: position_id={position_id}")
        
        position = self.position_repo.get_by_id(position_id)
        if not position:
            return None
        
        # 更新岗位
        for key, value in position_data.items():
            if hasattr(position, key):
                setattr(position, key, value)
        
        return self.position_repo.update(position)
    
    def delete_position(self, position_id: str) -> bool:
        """
        删除岗位
        
        Args:
            position_id: 岗位ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除岗位: position_id={position_id}")
        return self.position_repo.delete(position_id)
    
    def list_positions(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                      page: int = 1, page_size: int = 10) -> List[Position]:
        """
        获取岗位列表
        
        Args:
            tenant_id: 租户ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Position]: 岗位列表
        """
        if keyword:
            return self.position_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.position_repo.get_by_tenant_id(tenant_id, page, page_size)
        else:
            return self.position_repo.get_all(page, page_size)
    
    def count_positions(self, tenant_id: Optional[str] = None) -> int:
        """
        统计岗位数量
        
        Args:
            tenant_id: 租户ID（可选）
        
        Returns:
            int: 岗位数量
        """
        if tenant_id:
            return self.position_repo.count_by_tenant(tenant_id)
        else:
            return self.position_repo.count_all()