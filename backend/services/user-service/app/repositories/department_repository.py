# -*- coding: utf-8 -*-
"""
部门数据访问层

功能说明：
1. 部门CRUD操作
2. 部门树形结构查询
3. 部门统计操作

使用示例：
    from app.repositories.department_repository import DepartmentRepository
    
    dept_repo = DepartmentRepository(db)
    dept = dept_repo.get_by_code("tech")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models import Department


class DepartmentRepository:
    """
    部门数据访问层
    
    功能：
    - 部门CRUD操作
    - 部门树形结构查询
    - 部门统计操作
    
    使用方法：
        dept_repo = DepartmentRepository(db)
        dept = dept_repo.get_by_code("tech")
    """
    
    def __init__(self, db: Session):
        """
        初始化部门数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, department: Department) -> Department:
        """
        创建部门
        
        Args:
            department: 部门对象
        
        Returns:
            Department: 创建的部门对象
        """
        logger.info(f"创建部门: name={department.name}, code={department.code}, tenant_id={department.tenant_id}")
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department
    
    def get_by_id(self, department_id: str) -> Optional[Department]:
        """
        根据ID获取部门
        
        Args:
            department_id: 部门ID
        
        Returns:
            Optional[Department]: 部门对象，不存在返回None
        """
        return self.db.query(Department).filter(Department.id == department_id).first()
    
    def get_by_code(self, code: str) -> Optional[Department]:
        """
        根据编码获取部门
        
        Args:
            code: 部门编码
        
        Returns:
            Optional[Department]: 部门对象，不存在返回None
        """
        return self.db.query(Department).filter(Department.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        根据租户ID获取部门列表
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Department]: 部门列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).filter(Department.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_parent_id(self, parent_id: str, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        根据父部门ID获取子部门列表
        
        Args:
            parent_id: 父部门ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Department]: 部门列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).filter(Department.parent_id == parent_id).offset(offset).limit(page_size).all()
    
    def get_root_departments(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        获取租户的根部门（没有父部门的部门）
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Department]: 部门列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).filter(
            and_(
                Department.tenant_id == tenant_id,
                Department.parent_id.is_(None)
            )
        ).offset(offset).limit(page_size).all()
    
    def get_tree(self, tenant_id: str) -> List[Department]:
        """
        获取租户的部门树
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Department]: 部门树
        """
        root_departments = self.get_root_departments(tenant_id, page=1, page_size=1000)
        return root_departments
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        搜索部门
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Department]: 部门列表
        """
        offset = (page - 1) * page_size
        query = self.db.query(Department).filter(
            or_(
                Department.name.like(f"%{keyword}%"),
                Department.code.like(f"%{keyword}%"),
                Department.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(Department.tenant_id == tenant_id)
        
        return query.offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        获取所有部门
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Department]: 部门列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).offset(offset).limit(page_size).all()
    
    def update(self, department: Department) -> Department:
        """
        更新部门
        
        Args:
            department: 部门对象
        
        Returns:
            Department: 更新后的部门对象
        """
        logger.info(f"更新部门: department_id={department.id}")
        self.db.commit()
        self.db.refresh(department)
        return department
    
    def delete(self, department_id: str) -> bool:
        """
        删除部门
        
        Args:
            department_id: 部门ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除部门: department_id={department_id}")
        department = self.get_by_id(department_id)
        if not department:
            return False
        
        # 检查是否有子部门
        if department.children:
            raise ValueError("无法删除部门：该部门下存在子部门")
        
        # 检查是否有用户
        if department.users:
            raise ValueError("无法删除部门：该部门下存在用户")
        
        self.db.delete(department)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        统计租户部门数量
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            int: 部门数量
        """
        return self.db.query(Department).filter(Department.tenant_id == tenant_id).count()
    
    def count_by_parent(self, parent_id: str) -> int:
        """
        统计子部门数量
        
        Args:
            parent_id: 父部门ID
        
        Returns:
            int: 子部门数量
        """
        return self.db.query(Department).filter(Department.parent_id == parent_id).count()
    
    def count_all(self) -> int:
        """
        统计所有部门数量
        
        Returns:
            int: 部门数量
        """
        return self.db.query(Department).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        检查部门编码是否存在
        
        Args:
            code: 部门编码
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Department).filter(Department.code == code).first() is not None
    
    def exists_by_name_in_tenant(self, name: str, tenant_id: str) -> bool:
        """
        检查租户内部门名称是否存在
        
        Args:
            name: 部门名称
            tenant_id: 租户ID
        
        Returns:
            bool: 是否存在
        """
        return self.db.query(Department).filter(
            and_(
                Department.name == name,
                Department.tenant_id == tenant_id
            )
        ).first() is not None