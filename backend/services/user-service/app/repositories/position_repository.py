# -*- coding: utf-8 -*-
"""
岗位数据访问层

功能说明：
1. 岗位CRUD操作
2. 岗位查询操作
3. 岗位统计操作

使用示例：
    from app.repositories.position_repository import PositionRepository
    
    position_repo = PositionRepository(db)
    position = position_repo.get_by_code("developer")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models.position import Position


class PositionRepository:
    """
    岗位数据访问层
    
    功能：
    - 岗位CRUD操作
    - 岗位查询操作
    - 岗位统计操作
    
    使用方法：
        position_repo = PositionRepository(db)
        position = position_repo.get_by_code("developer")
    """
    
    def __init__(self, db: Session):
        """
        初始化岗位数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, position: Position) -> Position:
        """
        创建岗位
        
        Args:
            position: 岗位对象
        
        Returns:
            Position: 创建的岗位对象
        """
        logger.info(f"创建岗位: name={position.name}, code={position.code}, tenant_id={position.tenant_id}")
        self.db.add(position)
        self.db.commit()
        self.db.refresh(position)
        return position
    
    def get_by_id(self, position_id: str) -> Optional[Position]:
        """
        根据ID获取岗位
        
        Args:
            position_id: 岗位ID
        
        Returns:
            Optional[Position]: 岗位对象，不存在返回None
        """
        return self.db.query(Position).filter(Position.id == position_id).first()
    
    def get_by_code(self, code: str) -> Optional[Position]:
        """
        根据编码获取岗位
        
        Args:
            code: 岗位编码
        
        Returns:
            Optional[Position]: 岗位对象，不存在返回None
        """
        return self.db.query(Position).filter(Position.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Position]:
        """
        根据租户ID获取岗位列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Position]: 岗位列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Position).filter(Position.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Position]:
        """
        搜索岗位
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Position]: 岗位列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(Position).filter(
            or_(
                Position.name.like(f"%{keyword}%"),
                Position.code.like(f"%{keyword}%"),
                Position.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Position.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Position]:
        """
        获取所有岗位
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Position]: 岗位列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Position).offset(offset).limit(page_size).all()
    
    def update(self, position: Position) -> Position:
        """
        更新岗位
        
        Args:
            position: 岗位对象
        
        Returns:
            Position: 更新后的岗位对象
        """
        logger.info(f"更新岗位: position_id={position.id}")
        self.db.commit()
        self.db.refresh(position)
        return position
    
    def delete(self, position_id: str) -> bool:
        """
        删除岗位
        
        Args:
            position_id: 岗位ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除岗位: position_id={position_id}")
        position = self.get_by_id(position_id)
        if not position:
            return False
        
        self.db.delete(position)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户岗位数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 岗位数量
        """
        return self.db.query(Position).filter(Position.tenant_id == tenant_id).count()
    
    def count_all(self) -> int:
        """
        统计所有岗位数量
        
        Returns:
            int: 岗位数量
        """
        return self.db.query(Position).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查岗位编码是否存在
        
        Args:
            code: 岗位编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Position).filter(Position.code == code).first() is not None