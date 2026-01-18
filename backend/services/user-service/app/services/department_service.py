# -*- coding: utf-8 -*-
"""
部门业务逻辑层

功能说明：
1. 部门CRUD操作
2. 部门树形结构管理
3. 部门层级自动计算
4. 部门编码自动生成
5. 部门删除验证

使用示例：
    from app.services.department_service import DepartmentService
    
    dept_service = DepartmentService(db)
    dept = dept_service.create_department({
        "name": "技术部",
        "tenant_id": "tenant_001"
    })
"""

from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from loguru import logger

from common.database.models import Department
from app.repositories.department_repository import DepartmentRepository


class DepartmentService:
    """
    部门业务逻辑层
    
    功能：
    - 部门CRUD操作
    - 部门树形结构管理
    - 部门层级自动计算
    - 部门编码自动生成
    - 部门删除验证
    
    使用方法：
        dept_service = DepartmentService(db)
        dept = dept_service.create_department({
            "name": "技术部",
            "tenant_id": "tenant_001"
        })
    """
    
    def __init__(self, db: Session):
        """
        初始化部门业务逻辑层
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.dept_repo = DepartmentRepository(db)
    
    def create_department(self, dept_data: Dict) -> Department:
        """
        创建部门
        
        功能：
        - 验证部门编码唯一性
        - 验证部门名称在租户内唯一性
        - 自动计算部门层级
        - 自动生成部门编码（如果未提供）
        
        Args:
            dept_data: 部门数据
                - name: 部门名称（必填）
                - code: 部门编码（可选，自动生成）
                - tenant_id: 租户ID（必填）
                - parent_id: 父部门ID（可选）
                - level: 层级（可选，自动计算）
                - sort_order: 排序（可选）
                - description: 描述（可选）
                - leader_id: 负责人ID（可选）
                - phone: 联系电话（可选）
                - email: 联系邮箱（可选）
        
        Returns:
            Department: 创建的部门对象
        
        Raises:
            ValueError: 部门编码已存在或部门名称已存在
        """
        logger.info(f"创建部门: name={dept_data.get('name')}, tenant_id={dept_data.get('tenant_id')}")
        
        # 验证必填字段
        if not dept_data.get('name'):
            raise ValueError("部门名称不能为空")
        
        if not dept_data.get('tenant_id'):
            raise ValueError("租户ID不能为空")
        
        # 检查部门编码是否存在
        code = dept_data.get('code')
        if code and self.dept_repo.exists_by_code(code):
            raise ValueError(f"部门编码已存在: {code}")
        
        # 检查部门名称在租户内是否存在
        if self.dept_repo.exists_by_name_in_tenant(dept_data['name'], dept_data['tenant_id']):
            raise ValueError(f"部门名称已存在: {dept_data['name']}")
        
        # 自动生成部门编码
        if not code:
            code = self._generate_code(dept_data['tenant_id'], dept_data.get('parent_id'))
            dept_data['code'] = code
        
        # 自动计算部门层级
        parent_id = dept_data.get('parent_id')
        if parent_id:
            parent = self.dept_repo.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"父部门不存在: {parent_id}")
            if parent.tenant_id != dept_data['tenant_id']:
                raise ValueError("父部门与当前部门不在同一租户")
            dept_data['level'] = parent.level + 1
        else:
            dept_data['level'] = 1
        
        # 创建部门
        department = Department(
            tenant_id=dept_data['tenant_id'],
            parent_id=dept_data.get('parent_id'),
            name=dept_data['name'],
            code=dept_data['code'],
            level=dept_data['level'],
            sort_order=dept_data.get('sort_order', 0),
            description=dept_data.get('description'),
            leader_id=dept_data.get('leader_id'),
            phone=dept_data.get('phone'),
            email=dept_data.get('email')
        )
        
        return self.dept_repo.create(department)
    
    def get_department(self, department_id: str) -> Optional[Department]:
        """
        获取部门详情
        
        Args:
            department_id: 部门ID
        
        Returns:
            Optional[Department]: 部门对象，不存在返回None
        """
        return self.dept_repo.get_by_id(department_id)
    
    def update_department(self, department_id: str, dept_data: Dict) -> Department:
        """
        更新部门
        
        功能：
        - 验证部门编码唯一性（如果修改了编码）
        - 验证部门名称在租户内唯一性（如果修改了名称）
        - 自动计算部门层级（如果修改了父部门）
        
        Args:
            department_id: 部门ID
            dept_data: 部门数据
        
        Returns:
            Department: 更新后的部门对象
        
        Raises:
            ValueError: 部门不存在或验证失败
        """
        logger.info(f"更新部门: department_id={department_id}")
        
        # 获取部门
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise ValueError(f"部门不存在: {department_id}")
        
        # 更新部门名称
        if dept_data.get('name') and dept_data['name'] != department.name:
            # 检查部门名称在租户内是否存在
            if self.dept_repo.exists_by_name_in_tenant(dept_data['name'], department.tenant_id):
                raise ValueError(f"部门名称已存在: {dept_data['name']}")
            department.name = dept_data['name']
        
        # 更新部门编码
        if dept_data.get('code') and dept_data['code'] != department.code:
            # 检查部门编码是否存在
            if self.dept_repo.exists_by_code(dept_data['code']):
                raise ValueError(f"部门编码已存在: {dept_data['code']}")
            department.code = dept_data['code']
        
        # 更新父部门
        if dept_data.get('parent_id') != department.parent_id:
            new_parent_id = dept_data.get('parent_id')
            
            # 检查是否将部门设置为自己的子部门
            if new_parent_id:
                if self._is_descendant(department_id, new_parent_id):
                    raise ValueError("不能将部门设置为自己的子部门")
                
                parent = self.dept_repo.get_by_id(new_parent_id)
                if not parent:
                    raise ValueError(f"父部门不存在: {new_parent_id}")
                if parent.tenant_id != department.tenant_id:
                    raise ValueError("父部门与当前部门不在同一租户")
                
                department.parent_id = new_parent_id
                department.level = parent.level + 1
            else:
                department.parent_id = None
                department.level = 1
            
            # 更新所有子部门的层级
            self._update_children_level(department_id)
        
        # 更新其他字段
        if dept_data.get('sort_order') is not None:
            department.sort_order = dept_data['sort_order']
        
        if dept_data.get('description') is not None:
            department.description = dept_data['description']
        
        if dept_data.get('leader_id') is not None:
            department.leader_id = dept_data['leader_id']
        
        if dept_data.get('phone') is not None:
            department.phone = dept_data['phone']
        
        if dept_data.get('email') is not None:
            department.email = dept_data['email']
        
        return self.dept_repo.update(department)
    
    def delete_department(self, department_id: str) -> bool:
        """
        删除部门
        
        功能：
        - 检查部门是否存在
        - 检查是否有子部门
        - 检查是否有用户
        
        Args:
            department_id: 部门ID
        
        Returns:
            bool: 删除是否成功
        
        Raises:
            ValueError: 部门不存在或有子部门或有用户
        """
        logger.info(f"删除部门: department_id={department_id}")
        
        # 获取部门
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise ValueError(f"部门不存在: {department_id}")
        
        # 检查是否有子部门
        if department.children:
            raise ValueError("无法删除部门：该部门下存在子部门")
        
        # 检查是否有用户
        if department.users:
            raise ValueError("无法删除部门：该部门下存在用户")
        
        return self.dept_repo.delete(department_id)
    
    def list_departments(
        self,
        tenant_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        获取部门列表
        
        Args:
            tenant_id: 租户ID（可选）
            parent_id: 父部门ID（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            Dict: 部门列表
                - total: 总数
                - items: 部门列表
                - page: 页码
                - page_size: 每页数量
        """
        # 根据条件查询
        if keyword:
            departments = self.dept_repo.search(keyword, tenant_id, page, page_size)
            total = len(departments)  # TODO: 需要优化，应该单独查询总数
        elif tenant_id and parent_id:
            departments = self.dept_repo.get_by_parent_id(parent_id, page, page_size)
            total = self.dept_repo.count_by_parent(parent_id)
        elif tenant_id:
            departments = self.dept_repo.get_by_tenant_id(tenant_id, page, page_size)
            total = self.dept_repo.count_by_tenant(tenant_id)
        else:
            departments = self.dept_repo.get_all(page, page_size)
            total = self.dept_repo.count_all()
        
        return {
            "total": total,
            "items": [dept.to_dict() for dept in departments],
            "page": page,
            "page_size": page_size
        }
    
    def get_department_tree(self, tenant_id: str) -> List[Dict]:
        """
        获取部门树
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Dict]: 部门树
        """
        root_departments = self.dept_repo.get_tree(tenant_id)
        return [dept.to_tree_dict() for dept in root_departments]
    
    def _generate_code(self, tenant_id: str, parent_id: Optional[str] = None) -> str:
        """
        自动生成部门编码
        
        规则：
        - 根部门：DEPT_{租户ID}_{序号}
        - 子部门：{父部门编码}_{序号}
        
        Args:
            tenant_id: 租户ID
            parent_id: 父部门ID
        
        Returns:
            str: 部门编码
        """
        if parent_id:
            # 子部门编码
            parent = self.dept_repo.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"父部门不存在: {parent_id}")
            
            # 获取同级部门数量
            siblings_count = self.dept_repo.count_by_parent(parent_id)
            code = f"{parent.code}_{siblings_count + 1:03d}"
        else:
            # 根部门编码
            root_count = self.dept_repo.count_by_tenant(tenant_id)
            code = f"DEPT_{tenant_id}_{root_count + 1:03d}"
        
        # 检查编码是否已存在
        if self.dept_repo.exists_by_code(code):
            # 如果已存在，递归生成新的编码
            return self._generate_code(tenant_id, parent_id)
        
        return code
    
    def _is_descendant(self, department_id: str, child_id: str) -> bool:
        """
        检查child_id是否是department_id的子孙部门
        
        Args:
            department_id: 部门ID
            child_id: 子部门ID
        
        Returns:
            bool: 是否是子孙部门
        """
        if department_id == child_id:
            return True
        
        child = self.dept_repo.get_by_id(child_id)
        if not child or not child.parent_id:
            return False
        
        return self._is_descendant(department_id, child.parent_id)
    
    def _update_children_level(self, department_id: str):
        """
        递归更新子部门的层级
        
        Args:
            department_id: 部门ID
        """
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            return
        
        for child in department.children:
            child.level = department.level + 1
            self.dept_repo.update(child)
            self._update_children_level(child.id)