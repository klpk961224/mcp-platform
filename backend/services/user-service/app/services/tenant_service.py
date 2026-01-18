# -*- coding: utf-8 -*-
"""
租户业务逻辑层

功能说明：
1. 租户CRUD操作
2. 租户套餐管理
3. 租户资源配额管理
4. 租户状态管理
5. 租户过期检查

使用示例：
    from app.services.tenant_service import TenantService
    
    tenant_service = TenantService(db)
    tenant = tenant_service.create_tenant({
        "name": "示例公司",
        "code": "example"
    })
"""

from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from loguru import logger

from common.database.models import Tenant
from app.repositories.tenant_repository import TenantRepository


class TenantService:
    """
    租户业务逻辑层
    
    功能：
    - 租户CRUD操作
    - 租户套餐管理
    - 租户资源配额管理
    - 租户状态管理
    - 租户过期检查
    
    使用方法：
        tenant_service = TenantService(db)
        tenant = tenant_service.create_tenant({
            "name": "示例公司",
            "code": "example"
        })
    """
    
    # 预定义套餐配置
    PACKAGES = {
        "free": {
            "name": "免费版",
            "max_users": 10,
            "max_departments": 5,
            "max_storage": 1024,  # 1GB
            "duration_days": 30
        },
        "basic": {
            "name": "基础版",
            "max_users": 50,
            "max_departments": 20,
            "max_storage": 10240,  # 10GB
            "duration_days": 365
        },
        "professional": {
            "name": "专业版",
            "max_users": 200,
            "max_departments": 100,
            "max_storage": 102400,  # 100GB
            "duration_days": 365
        },
        "enterprise": {
            "name": "企业版",
            "max_users": 1000,
            "max_departments": 500,
            "max_storage": 1024000,  # 1TB
            "duration_days": 365
        }
    }
    
    def __init__(self, db: Session):
        """
        初始化租户业务逻辑层
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.tenant_repo = TenantRepository(db)
    
    def create_tenant(self, tenant_data: Dict) -> Tenant:
        """
        创建租户
        
        功能：
        - 验证租户编码唯一性
        - 验证租户名称唯一性
        - 自动应用套餐配置
        - 自动计算过期时间
        
        Args:
            tenant_data: 租户数据
                - name: 租户名称（必填）
                - code: 租户编码（必填）
                - description: 描述（可选）
                - package_id: 套餐ID（可选，默认basic）
                - status: 状态（可选，默认active）
        
        Returns:
            Tenant: 创建的租户对象
        
        Raises:
            ValueError: 租户编码已存在或租户名称已存在
        """
        logger.info(f"创建租户: name={tenant_data.get('name')}, code={tenant_data.get('code')}")
        
        # 验证必填字段
        if not tenant_data.get('name'):
            raise ValueError("租户名称不能为空")
        
        if not tenant_data.get('code'):
            raise ValueError("租户编码不能为空")
        
        # 检查租户编码是否存在
        if self.tenant_repo.exists_by_code(tenant_data['code']):
            raise ValueError(f"租户编码已存在: {tenant_data['code']}")
        
        # 检查租户名称是否存在
        if self.tenant_repo.exists_by_name(tenant_data['name']):
            raise ValueError(f"租户名称已存在: {tenant_data['name']}")
        
        # 获取套餐配置
        package_id = tenant_data.get('package_id', 'basic')
        package_config = self.PACKAGES.get(package_id, self.PACKAGES['basic'])
        
        # 计算过期时间
        expires_at = None
        if tenant_data.get('status') == 'active':
            duration_days = package_config['duration_days']
            expires_at = datetime.now() + timedelta(days=duration_days)
        
        # 创建租户
        tenant = Tenant(
            name=tenant_data['name'],
            code=tenant_data['code'],
            status=tenant_data.get('status', 'active'),
            description=tenant_data.get('description'),
            package_id=package_id,
            max_users=package_config['max_users'],
            max_departments=package_config['max_departments'],
            max_storage=package_config['max_storage'],
            expires_at=expires_at
        )
        
        return self.tenant_repo.create(tenant)
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """
        获取租户详情
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Optional[Tenant]: 租户对象，不存在返回None
        """
        return self.tenant_repo.get_by_id(tenant_id)
    
    def update_tenant(self, tenant_id: str, tenant_data: Dict) -> Tenant:
        """
        更新租户
        
        功能：
        - 验证租户编码唯一性（如果修改了编码）
        - 验证租户名称唯一性（如果修改了名称）
        - 更新套餐配置（如果修改了套餐）
        - 重新计算过期时间（如果修改了状态或套餐）
        
        Args:
            tenant_id: 租户ID
            tenant_data: 租户数据
        
        Returns:
            Tenant: 更新后的租户对象
        
        Raises:
            ValueError: 租户不存在或验证失败
        """
        logger.info(f"更新租户: tenant_id={tenant_id}")
        
        # 获取租户
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"租户不存在: {tenant_id}")
        
        # 更新租户名称
        if tenant_data.get('name') and tenant_data['name'] != tenant.name:
            # 检查租户名称是否存在
            if self.tenant_repo.exists_by_name(tenant_data['name']):
                raise ValueError(f"租户名称已存在: {tenant_data['name']}")
            tenant.name = tenant_data['name']
        
        # 更新租户编码
        if tenant_data.get('code') and tenant_data['code'] != tenant.code:
            # 检查租户编码是否存在
            if self.tenant_repo.exists_by_code(tenant_data['code']):
                raise ValueError(f"租户编码已存在: {tenant_data['code']}")
            tenant.code = tenant_data['code']
        
        # 更新描述
        if tenant_data.get('description') is not None:
            tenant.description = tenant_data['description']
        
        # 更新状态
        if tenant_data.get('status') and tenant_data['status'] != tenant.status:
            tenant.status = tenant_data['status']
            # 重新计算过期时间
            if tenant.status == 'active':
                package_config = self.PACKAGES.get(tenant.package_id, self.PACKAGES['basic'])
                if not tenant.expires_at or tenant.expires_at < datetime.now():
                    duration_days = package_config['duration_days']
                    tenant.expires_at = datetime.now() + timedelta(days=duration_days)
        
        # 更新套餐
        if tenant_data.get('package_id') and tenant_data['package_id'] != tenant.package_id:
            package_id = tenant_data['package_id']
            package_config = self.PACKAGES.get(package_id, self.PACKAGES['basic'])
            tenant.package_id = package_id
            tenant.max_users = package_config['max_users']
            tenant.max_departments = package_config['max_departments']
            tenant.max_storage = package_config['max_storage']
            # 重新计算过期时间
            if tenant.status == 'active':
                duration_days = package_config['duration_days']
                tenant.expires_at = datetime.now() + timedelta(days=duration_days)
        
        return self.tenant_repo.update(tenant)
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """
        删除租户
        
        功能：
        - 检查租户是否存在
        - 检查是否有用户
        - 检查是否有部门
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            bool: 删除是否成功
        
        Raises:
            ValueError: 租户不存在或有用户或有部门
        """
        logger.info(f"删除租户: tenant_id={tenant_id}")
        
        # 获取租户
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"租户不存在: {tenant_id}")
        
        # 检查是否有用户
        if tenant.users:
            raise ValueError("无法删除租户：该租户下存在用户")
        
        # 检查是否有部门
        if tenant.departments:
            raise ValueError("无法删除租户：该租户下存在部门")
        
        return self.tenant_repo.delete(tenant_id)
    
    def list_tenants(
        self,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        获取租户列表
        
        Args:
            status: 状态（可选）
            keyword: 搜索关键词（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            Dict: 租户列表
                - total: 总数
                - items: 租户列表
                - page: 页码
                - page_size: 每页数量
        """
        # 根据条件查询
        if keyword:
            tenants = self.tenant_repo.search(keyword, page, page_size)
            total = len(tenants)  # TODO: 需要优化，应该单独查询总数
        elif status == 'active':
            tenants = self.tenant_repo.get_active_tenants(page, page_size)
            total = self.tenant_repo.count_active()
        elif status == 'expired':
            tenants = self.tenant_repo.get_expired_tenants(page, page_size)
            total = self.tenant_repo.count_expired()
        else:
            tenants = self.tenant_repo.get_all(page, page_size)
            total = self.tenant_repo.count_all()
        
        return {
            "total": total,
            "items": [tenant.to_dict() for tenant in tenants],
            "page": page,
            "page_size": page_size
        }
    
    def check_quota(self, tenant_id: str, quota_type: str) -> Dict:
        """
        检查租户资源配额
        
        Args:
            tenant_id: 租户ID
            quota_type: 配额类型（users/departments/storage）
        
        Returns:
            Dict: 配额信息
                - used: 已使用量
                - max: 最大配额
                - available: 可用量
                - percentage: 使用百分比
        """
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"租户不存在: {tenant_id}")
        
        if quota_type == 'users':
            used = tenant.get_user_count()
            max_quota = tenant.max_users
        elif quota_type == 'departments':
            used = tenant.get_department_count()
            max_quota = tenant.max_departments
        elif quota_type == 'storage':
            # TODO: 实现存储空间统计
            used = 0
            max_quota = tenant.max_storage
        else:
            raise ValueError(f"不支持的配额类型: {quota_type}")
        
        available = max_quota - used
        percentage = (used / max_quota * 100) if max_quota > 0 else 0
        
        return {
            "used": used,
            "max": max_quota,
            "available": available,
            "percentage": round(percentage, 2)
        }
    
    def get_package_info(self, package_id: str) -> Optional[Dict]:
        """
        获取套餐信息
        
        Args:
            package_id: 套餐ID
        
        Returns:
            Optional[Dict]: 套餐信息，不存在返回None
        """
        return self.PACKAGES.get(package_id)
    
    def get_all_packages(self) -> Dict:
        """
        获取所有套餐信息
        
        Returns:
            Dict: 所有套餐信息
        """
        return self.PACKAGES
    
    def update_package(self, tenant_id: str, package_id: str) -> Tenant:
        """
        更新租户套餐
        
        Args:
            tenant_id: 租户ID
            package_id: 套餐ID
        
        Returns:
            Tenant: 更新后的租户对象
        
        Raises:
            ValueError: 租户不存在或套餐不存在
        """
        # 检查套餐是否存在
        if package_id not in self.PACKAGES:
            raise ValueError(f"套餐不存在: {package_id}")
        
        # 更新租户套餐
        return self.update_tenant(tenant_id, {"package_id": package_id})
    
    def check_expiration(self, tenant_id: str) -> bool:
        """
        检查租户是否过期
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            bool: 是否已过期
        """
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            return False
        
        return tenant.is_expired()
    
    def renew_tenant(self, tenant_id: str, days: int = 365) -> Tenant:
        """
        续费租户
        
        Args:
            tenant_id: 租户ID
            days: 续费天数
        
        Returns:
            Tenant: 更新后的租户对象
        
        Raises:
            ValueError: 租户不存在
        """
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"租户不存在: {tenant_id}")
        
        # 如果租户已过期，从当前时间开始计算
        if tenant.is_expired():
            tenant.expires_at = datetime.now() + timedelta(days=days)
        else:
            # 如果租户未过期，在原有过期时间基础上延长
            tenant.expires_at = tenant.expires_at + timedelta(days=days)
        
        tenant.status = 'active'
        return self.tenant_repo.update(tenant)