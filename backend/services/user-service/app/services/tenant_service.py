# -*- coding: utf-8 -*-
"""
绉熸埛涓氬姟閫昏緫灞?
鍔熻兘璇存槑锛?1. 绉熸埛CRUD鎿嶄綔
2. 绉熸埛濂楅绠＄悊
3. 绉熸埛璧勬簮閰嶉绠＄悊
4. 绉熸埛鐘舵€佺鐞?5. 绉熸埛杩囨湡妫€鏌?
浣跨敤绀轰緥锛?    from app.services.tenant_service import TenantService
    
    tenant_service = TenantService(db)
    tenant = tenant_service.create_tenant({
        "name": "绀轰緥鍏徃",
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
    绉熸埛涓氬姟閫昏緫灞?    
    鍔熻兘锛?    - 绉熸埛CRUD鎿嶄綔
    - 绉熸埛濂楅绠＄悊
    - 绉熸埛璧勬簮閰嶉绠＄悊
    - 绉熸埛鐘舵€佺鐞?    - 绉熸埛杩囨湡妫€鏌?    
    浣跨敤鏂规硶锛?        tenant_service = TenantService(db)
        tenant = tenant_service.create_tenant({
            "name": "绀轰緥鍏徃",
            "code": "example"
        })
    """
    
    # 棰勫畾涔夊椁愰厤缃?    PACKAGES = {
        "free": {
            "name": "鍏嶈垂鐗?,
            "max_users": 10,
            "max_departments": 5,
            "max_storage": 1024,  # 1GB
            "duration_days": 30
        },
        "basic": {
            "name": "鍩虹鐗?,
            "max_users": 50,
            "max_departments": 20,
            "max_storage": 10240,  # 10GB
            "duration_days": 365
        },
        "professional": {
            "name": "涓撲笟鐗?,
            "max_users": 200,
            "max_departments": 100,
            "max_storage": 102400,  # 100GB
            "duration_days": 365
        },
        "enterprise": {
            "name": "浼佷笟鐗?,
            "max_users": 1000,
            "max_departments": 500,
            "max_storage": 1024000,  # 1TB
            "duration_days": 365
        }
    }
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栫鎴蜂笟鍔￠€昏緫灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.tenant_repo = TenantRepository(db)
    
    def create_tenant(self, tenant_data: Dict) -> Tenant:
        """
        鍒涘缓绉熸埛
        
        鍔熻兘锛?        - 楠岃瘉绉熸埛缂栫爜鍞竴鎬?        - 楠岃瘉绉熸埛鍚嶇О鍞竴鎬?        - 鑷姩搴旂敤濂楅閰嶇疆
        - 鑷姩璁＄畻杩囨湡鏃堕棿
        
        Args:
            tenant_data: 绉熸埛鏁版嵁
                - name: 绉熸埛鍚嶇О锛堝繀濉級
                - code: 绉熸埛缂栫爜锛堝繀濉級
                - description: 鎻忚堪锛堝彲閫夛級
                - package_id: 濂楅ID锛堝彲閫夛紝榛樿basic锛?                - status: 鐘舵€侊紙鍙€夛紝榛樿active锛?        
        Returns:
            Tenant: 鍒涘缓鐨勭鎴峰璞?        
        Raises:
            ValueError: 绉熸埛缂栫爜宸插瓨鍦ㄦ垨绉熸埛鍚嶇О宸插瓨鍦?        """
        logger.info(f"鍒涘缓绉熸埛: name={tenant_data.get('name')}, code={tenant_data.get('code')}")
        
        # 楠岃瘉蹇呭～瀛楁
        if not tenant_data.get('name'):
            raise ValueError("绉熸埛鍚嶇О涓嶈兘涓虹┖")
        
        if not tenant_data.get('code'):
            raise ValueError("绉熸埛缂栫爜涓嶈兘涓虹┖")
        
        # 妫€鏌ョ鎴风紪鐮佹槸鍚﹀瓨鍦?        if self.tenant_repo.exists_by_code(tenant_data['code']):
            raise ValueError(f"绉熸埛缂栫爜宸插瓨鍦? {tenant_data['code']}")
        
        # 妫€鏌ョ鎴峰悕绉版槸鍚﹀瓨鍦?        if self.tenant_repo.exists_by_name(tenant_data['name']):
            raise ValueError(f"绉熸埛鍚嶇О宸插瓨鍦? {tenant_data['name']}")
        
        # 鑾峰彇濂楅閰嶇疆
        package_id = tenant_data.get('package_id', 'basic')
        package_config = self.PACKAGES.get(package_id, self.PACKAGES['basic'])
        
        # 璁＄畻杩囨湡鏃堕棿
        expires_at = None
        if tenant_data.get('status') == 'active':
            duration_days = package_config['duration_days']
            expires_at = datetime.now() + timedelta(days=duration_days)
        
        # 鍒涘缓绉熸埛
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
        鑾峰彇绉熸埛璇︽儏
        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            Optional[Tenant]: 绉熸埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.tenant_repo.get_by_id(tenant_id)
    
    def update_tenant(self, tenant_id: str, tenant_data: Dict) -> Tenant:
        """
        鏇存柊绉熸埛
        
        鍔熻兘锛?        - 楠岃瘉绉熸埛缂栫爜鍞竴鎬э紙濡傛灉淇敼浜嗙紪鐮侊級
        - 楠岃瘉绉熸埛鍚嶇О鍞竴鎬э紙濡傛灉淇敼浜嗗悕绉帮級
        - 鏇存柊濂楅閰嶇疆锛堝鏋滀慨鏀逛簡濂楅锛?        - 閲嶆柊璁＄畻杩囨湡鏃堕棿锛堝鏋滀慨鏀逛簡鐘舵€佹垨濂楅锛?        
        Args:
            tenant_id: 绉熸埛ID
            tenant_data: 绉熸埛鏁版嵁
        
        Returns:
            Tenant: 鏇存柊鍚庣殑绉熸埛瀵硅薄
        
        Raises:
            ValueError: 绉熸埛涓嶅瓨鍦ㄦ垨楠岃瘉澶辫触
        """
        logger.info(f"鏇存柊绉熸埛: tenant_id={tenant_id}")
        
        # 鑾峰彇绉熸埛
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"绉熸埛涓嶅瓨鍦? {tenant_id}")
        
        # 鏇存柊绉熸埛鍚嶇О
        if tenant_data.get('name') and tenant_data['name'] != tenant.name:
            # 妫€鏌ョ鎴峰悕绉版槸鍚﹀瓨鍦?            if self.tenant_repo.exists_by_name(tenant_data['name']):
                raise ValueError(f"绉熸埛鍚嶇О宸插瓨鍦? {tenant_data['name']}")
            tenant.name = tenant_data['name']
        
        # 鏇存柊绉熸埛缂栫爜
        if tenant_data.get('code') and tenant_data['code'] != tenant.code:
            # 妫€鏌ョ鎴风紪鐮佹槸鍚﹀瓨鍦?            if self.tenant_repo.exists_by_code(tenant_data['code']):
                raise ValueError(f"绉熸埛缂栫爜宸插瓨鍦? {tenant_data['code']}")
            tenant.code = tenant_data['code']
        
        # 鏇存柊鎻忚堪
        if tenant_data.get('description') is not None:
            tenant.description = tenant_data['description']
        
        # 鏇存柊鐘舵€?        if tenant_data.get('status') and tenant_data['status'] != tenant.status:
            tenant.status = tenant_data['status']
            # 閲嶆柊璁＄畻杩囨湡鏃堕棿
            if tenant.status == 'active':
                package_config = self.PACKAGES.get(tenant.package_id, self.PACKAGES['basic'])
                if not tenant.expires_at or tenant.expires_at < datetime.now():
                    duration_days = package_config['duration_days']
                    tenant.expires_at = datetime.now() + timedelta(days=duration_days)
        
        # 鏇存柊濂楅
        if tenant_data.get('package_id') and tenant_data['package_id'] != tenant.package_id:
            package_id = tenant_data['package_id']
            package_config = self.PACKAGES.get(package_id, self.PACKAGES['basic'])
            tenant.package_id = package_id
            tenant.max_users = package_config['max_users']
            tenant.max_departments = package_config['max_departments']
            tenant.max_storage = package_config['max_storage']
            # 閲嶆柊璁＄畻杩囨湡鏃堕棿
            if tenant.status == 'active':
                duration_days = package_config['duration_days']
                tenant.expires_at = datetime.now() + timedelta(days=duration_days)
        
        return self.tenant_repo.update(tenant)
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """
        鍒犻櫎绉熸埛
        
        鍔熻兘锛?        - 妫€鏌ョ鎴锋槸鍚﹀瓨鍦?        - 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        - 妫€鏌ユ槸鍚︽湁閮ㄩ棬
        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        
        Raises:
            ValueError: 绉熸埛涓嶅瓨鍦ㄦ垨鏈夌敤鎴锋垨鏈夐儴闂?        """
        logger.info(f"鍒犻櫎绉熸埛: tenant_id={tenant_id}")
        
        # 鑾峰彇绉熸埛
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"绉熸埛涓嶅瓨鍦? {tenant_id}")
        
        # 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        if tenant.users:
            raise ValueError("鏃犳硶鍒犻櫎绉熸埛锛氳绉熸埛涓嬪瓨鍦ㄧ敤鎴?)
        
        # 妫€鏌ユ槸鍚︽湁閮ㄩ棬
        if tenant.departments:
            raise ValueError("鏃犳硶鍒犻櫎绉熸埛锛氳绉熸埛涓嬪瓨鍦ㄩ儴闂?)
        
        return self.tenant_repo.delete(tenant_id)
    
    def list_tenants(
        self,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        鑾峰彇绉熸埛鍒楄〃
        
        Args:
            status: 鐘舵€侊紙鍙€夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            Dict: 绉熸埛鍒楄〃
                - total: 鎬绘暟
                - items: 绉熸埛鍒楄〃
                - page: 椤电爜
                - page_size: 姣忛〉鏁伴噺
        """
        # 鏍规嵁鏉′欢鏌ヨ
        if keyword:
            tenants = self.tenant_repo.search(keyword, page, page_size)
            total = len(tenants)  # TODO: 闇€瑕佷紭鍖栵紝搴旇鍗曠嫭鏌ヨ鎬绘暟
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
        妫€鏌ョ鎴疯祫婧愰厤棰?        
        Args:
            tenant_id: 绉熸埛ID
            quota_type: 閰嶉绫诲瀷锛坲sers/departments/storage锛?        
        Returns:
            Dict: 閰嶉淇℃伅
                - used: 宸蹭娇鐢ㄩ噺
                - max: 鏈€澶ч厤棰?                - available: 鍙敤閲?                - percentage: 浣跨敤鐧惧垎姣?        """
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"绉熸埛涓嶅瓨鍦? {tenant_id}")
        
        if quota_type == 'users':
            used = tenant.get_user_count()
            max_quota = tenant.max_users
        elif quota_type == 'departments':
            used = tenant.get_department_count()
            max_quota = tenant.max_departments
        elif quota_type == 'storage':
            # TODO: 瀹炵幇瀛樺偍绌洪棿缁熻
            used = 0
            max_quota = tenant.max_storage
        else:
            raise ValueError(f"涓嶆敮鎸佺殑閰嶉绫诲瀷: {quota_type}")
        
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
        鑾峰彇濂楅淇℃伅
        
        Args:
            package_id: 濂楅ID
        
        Returns:
            Optional[Dict]: 濂楅淇℃伅锛屼笉瀛樺湪杩斿洖None
        """
        return self.PACKAGES.get(package_id)
    
    def get_all_packages(self) -> Dict:
        """
        鑾峰彇鎵€鏈夊椁愪俊鎭?        
        Returns:
            Dict: 鎵€鏈夊椁愪俊鎭?        """
        return self.PACKAGES
    
    def update_package(self, tenant_id: str, package_id: str) -> Tenant:
        """
        鏇存柊绉熸埛濂楅
        
        Args:
            tenant_id: 绉熸埛ID
            package_id: 濂楅ID
        
        Returns:
            Tenant: 鏇存柊鍚庣殑绉熸埛瀵硅薄
        
        Raises:
            ValueError: 绉熸埛涓嶅瓨鍦ㄦ垨濂楅涓嶅瓨鍦?        """
        # 妫€鏌ュ椁愭槸鍚﹀瓨鍦?        if package_id not in self.PACKAGES:
            raise ValueError(f"濂楅涓嶅瓨鍦? {package_id}")
        
        # 鏇存柊绉熸埛濂楅
        return self.update_tenant(tenant_id, {"package_id": package_id})
    
    def check_expiration(self, tenant_id: str) -> bool:
        """
        妫€鏌ョ鎴锋槸鍚﹁繃鏈?        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            bool: 鏄惁宸茶繃鏈?        """
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            return False
        
        return tenant.is_expired()
    
    def renew_tenant(self, tenant_id: str, days: int = 365) -> Tenant:
        """
        缁垂绉熸埛
        
        Args:
            tenant_id: 绉熸埛ID
            days: 缁垂澶╂暟
        
        Returns:
            Tenant: 鏇存柊鍚庣殑绉熸埛瀵硅薄
        
        Raises:
            ValueError: 绉熸埛涓嶅瓨鍦?        """
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError(f"绉熸埛涓嶅瓨鍦? {tenant_id}")
        
        # 濡傛灉绉熸埛宸茶繃鏈燂紝浠庡綋鍓嶆椂闂村紑濮嬭绠?        if tenant.is_expired():
            tenant.expires_at = datetime.now() + timedelta(days=days)
        else:
            # 濡傛灉绉熸埛鏈繃鏈燂紝鍦ㄥ師鏈夎繃鏈熸椂闂村熀纭€涓婂欢闀?            tenant.expires_at = tenant.expires_at + timedelta(days=days)
        
        tenant.status = 'active'
        return self.tenant_repo.update(tenant)
