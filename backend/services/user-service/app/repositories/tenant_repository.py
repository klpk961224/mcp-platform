# -*- coding: utf-8 -*-
"""
绉熸埛鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 绉熸埛CRUD鎿嶄綔
2. 绉熸埛查询鎿嶄綔
3. 绉熸埛缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.tenant_repository import TenantRepository
    
    tenant_repo = TenantRepository(db)
    tenant = tenant_repo.get_by_code("example")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from loguru import logger

from common.database.models import Tenant


class TenantRepository:
    """
    绉熸埛鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 绉熸埛CRUD鎿嶄綔
    - 绉熸埛查询鎿嶄綔
    - 绉熸埛缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        tenant_repo = TenantRepository(db)
        tenant = tenant_repo.get_by_code("example")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栫鎴锋暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, tenant: Tenant) -> Tenant:
        """
        创建绉熸埛
        
        Args:
            tenant: 绉熸埛瀵硅薄
        
        Returns:
            Tenant: 创建鐨勭鎴峰璞?        """
        logger.info(f"创建绉熸埛: name={tenant.name}, code={tenant.code}")
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def get_by_id(self, tenant_id: str) -> Optional[Tenant]:
        """
        根据ID鑾峰彇绉熸埛
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            Optional[Tenant]: 绉熸埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    def get_by_code(self, code: str) -> Optional[Tenant]:
        """
        根据编码鑾峰彇绉熸埛
        
        Args:
            code: 绉熸埛编码
        
        Returns:
            Optional[Tenant]: 绉熸埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Tenant).filter(Tenant.code == code).first()
    
    def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        根据名称鑾峰彇绉熸埛
        
        Args:
            name: 绉熸埛名称
        
        Returns:
            Optional[Tenant]: 绉熸埛瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Tenant).filter(Tenant.name == name).first()
    
    def get_by_package_id(self, package_id: str, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        根据濂楅ID鑾峰彇绉熸埛鍒楄〃
        
        Args:
            package_id: 濂楅ID
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Tenant]: 绉熸埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(Tenant.package_id == package_id).offset(offset).limit(page_size).all()
    
    def get_active_tenants(self, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        鑾峰彇婵€娲荤殑绉熸埛鍒楄〃
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Tenant]: 绉熸埛鍒楄〃
        """
        from datetime import datetime
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(
            and_(
                Tenant.status == "active",
                or_(
                    Tenant.expires_at.is_(None),
                    Tenant.expires_at > datetime.now()
                )
            )
        ).offset(offset).limit(page_size).all()
    
    def get_expired_tenants(self, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        鑾峰彇杩囨湡鐨勭鎴峰垪琛?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Tenant]: 绉熸埛鍒楄〃
        """
        from datetime import datetime
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(
            and_(
                Tenant.expires_at.isnot(None),
                Tenant.expires_at < datetime.now()
            )
        ).offset(offset).limit(page_size).all()
    
    def search(self, keyword: str, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        鎼滅储绉熸埛
        
        Args:
            keyword: 鍏抽敭璇?            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Tenant]: 绉熸埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Tenant).filter(
            or_(
                Tenant.name.like(f"%{keyword}%"),
                Tenant.code.like(f"%{keyword}%"),
                Tenant.description.like(f"%{keyword}%")
            )
        ).offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Tenant]:
        """
        鑾峰彇鎵€鏈夌鎴?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Tenant]: 绉熸埛鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Tenant).offset(offset).limit(page_size).all()
    
    def update(self, tenant: Tenant) -> Tenant:
        """
        更新绉熸埛
        
        Args:
            tenant: 绉熸埛瀵硅薄
        
        Returns:
            Tenant: 更新鍚庣殑绉熸埛瀵硅薄
        """
        logger.info(f"更新绉熸埛: tenant_id={tenant.id}")
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def delete(self, tenant_id: str) -> bool:
        """
        删除绉熸埛
        
        Args:
            tenant_id: 租户ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除绉熸埛: tenant_id={tenant_id}")
        tenant = self.get_by_id(tenant_id)
        if not tenant:
            return False
        
        # 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        if tenant.users:
            raise ValueError("鏃犳硶删除绉熸埛锛氳绉熸埛涓嬪瓨鍦ㄧ敤鎴?)
        
        # 妫€鏌ユ槸鍚︽湁閮ㄩ棬
        if tenant.departments:
            raise ValueError("鏃犳硶删除绉熸埛锛氳绉熸埛涓嬪瓨鍦ㄩ儴闂?)
        
        self.db.delete(tenant)
        self.db.commit()
        return True
    
    def count_by_package(self, package_id: str) -> int:
        """
        缁熻濂楅绉熸埛数量
        
        Args:
            package_id: 濂楅ID
        
        Returns:
            int: 绉熸埛数量
        """
        return self.db.query(Tenant).filter(Tenant.package_id == package_id).count()
    
    def count_active(self) -> int:
        """
        缁熻婵€娲荤殑绉熸埛数量
        
        Returns:
            int: 绉熸埛数量
        """
        from datetime import datetime
        return self.db.query(Tenant).filter(
            and_(
                Tenant.status == "active",
                or_(
                    Tenant.expires_at.is_(None),
                    Tenant.expires_at > datetime.now()
                )
            )
        ).count()
    
    def count_expired(self) -> int:
        """
        缁熻杩囨湡鐨勭鎴锋暟閲?        
        Returns:
            int: 绉熸埛数量
        """
        from datetime import datetime
        return self.db.query(Tenant).filter(
            and_(
                Tenant.expires_at.isnot(None),
                Tenant.expires_at < datetime.now()
            )
        ).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夌鎴锋暟閲?        
        Returns:
            int: 绉熸埛数量
        """
        return self.db.query(Tenant).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€鏌ョ鎴风紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 绉熸埛编码
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Tenant).filter(Tenant.code == code).first() is not None
    
    def exists_by_name(self, name: str) -> bool:
        """
        妫€鏌ョ鎴峰悕绉版槸鍚﹀瓨鍦?        
        Args:
            name: 绉熸埛名称
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Tenant).filter(Tenant.name == name).first() is not None
