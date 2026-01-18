# -*- coding: utf-8 -*-
"""
閮ㄩ棬鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 閮ㄩ棬CRUD鎿嶄綔
2. 閮ㄩ棬鏍戝舰缁撴瀯鏌ヨ
3. 閮ㄩ棬缁熻鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.department_repository import DepartmentRepository
    
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
    閮ㄩ棬鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 閮ㄩ棬CRUD鎿嶄綔
    - 閮ㄩ棬鏍戝舰缁撴瀯鏌ヨ
    - 閮ㄩ棬缁熻鎿嶄綔
    
    浣跨敤鏂规硶锛?        dept_repo = DepartmentRepository(db)
        dept = dept_repo.get_by_code("tech")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栭儴闂ㄦ暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create(self, department: Department) -> Department:
        """
        鍒涘缓閮ㄩ棬
        
        Args:
            department: 閮ㄩ棬瀵硅薄
        
        Returns:
            Department: 鍒涘缓鐨勯儴闂ㄥ璞?        """
        logger.info(f"鍒涘缓閮ㄩ棬: name={department.name}, code={department.code}, tenant_id={department.tenant_id}")
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department
    
    def get_by_id(self, department_id: str) -> Optional[Department]:
        """
        鏍规嵁ID鑾峰彇閮ㄩ棬
        
        Args:
            department_id: 閮ㄩ棬ID
        
        Returns:
            Optional[Department]: 閮ㄩ棬瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Department).filter(Department.id == department_id).first()
    
    def get_by_code(self, code: str) -> Optional[Department]:
        """
        鏍规嵁缂栫爜鑾峰彇閮ㄩ棬
        
        Args:
            code: 閮ㄩ棬缂栫爜
        
        Returns:
            Optional[Department]: 閮ㄩ棬瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Department).filter(Department.code == code).first()
    
    def get_by_tenant_id(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        鏍规嵁绉熸埛ID鑾峰彇閮ㄩ棬鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Department]: 閮ㄩ棬鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).filter(Department.tenant_id == tenant_id).offset(offset).limit(page_size).all()
    
    def get_by_parent_id(self, parent_id: str, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        鏍规嵁鐖堕儴闂↖D鑾峰彇瀛愰儴闂ㄥ垪琛?        
        Args:
            parent_id: 鐖堕儴闂↖D
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Department]: 閮ㄩ棬鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).filter(Department.parent_id == parent_id).offset(offset).limit(page_size).all()
    
    def get_root_departments(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        鑾峰彇绉熸埛鐨勬牴閮ㄩ棬锛堟病鏈夌埗閮ㄩ棬鐨勯儴闂級
        
        Args:
            tenant_id: 绉熸埛ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Department]: 閮ㄩ棬鍒楄〃
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
        鑾峰彇绉熸埛鐨勯儴闂ㄦ爲
        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            List[Department]: 閮ㄩ棬鏍?        """
        root_departments = self.get_root_departments(tenant_id, page=1, page_size=1000)
        return root_departments
    
    def search(self, keyword: str, tenant_id: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Department]:
        """
        鎼滅储閮ㄩ棬
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 绉熸埛ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Department]: 閮ㄩ棬鍒楄〃
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
        鑾峰彇鎵€鏈夐儴闂?        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Department]: 閮ㄩ棬鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Department).offset(offset).limit(page_size).all()
    
    def update(self, department: Department) -> Department:
        """
        鏇存柊閮ㄩ棬
        
        Args:
            department: 閮ㄩ棬瀵硅薄
        
        Returns:
            Department: 鏇存柊鍚庣殑閮ㄩ棬瀵硅薄
        """
        logger.info(f"鏇存柊閮ㄩ棬: department_id={department.id}")
        self.db.commit()
        self.db.refresh(department)
        return department
    
    def delete(self, department_id: str) -> bool:
        """
        鍒犻櫎閮ㄩ棬
        
        Args:
            department_id: 閮ㄩ棬ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎閮ㄩ棬: department_id={department_id}")
        department = self.get_by_id(department_id)
        if not department:
            return False
        
        # 妫€鏌ユ槸鍚︽湁瀛愰儴闂?        if department.children:
            raise ValueError("鏃犳硶鍒犻櫎閮ㄩ棬锛氳閮ㄩ棬涓嬪瓨鍦ㄥ瓙閮ㄩ棬")
        
        # 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        if department.users:
            raise ValueError("鏃犳硶鍒犻櫎閮ㄩ棬锛氳閮ㄩ棬涓嬪瓨鍦ㄧ敤鎴?)
        
        self.db.delete(department)
        self.db.commit()
        return True
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """
        缁熻绉熸埛閮ㄩ棬鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID
        
        Returns:
            int: 閮ㄩ棬鏁伴噺
        """
        return self.db.query(Department).filter(Department.tenant_id == tenant_id).count()
    
    def count_by_parent(self, parent_id: str) -> int:
        """
        缁熻瀛愰儴闂ㄦ暟閲?        
        Args:
            parent_id: 鐖堕儴闂↖D
        
        Returns:
            int: 瀛愰儴闂ㄦ暟閲?        """
        return self.db.query(Department).filter(Department.parent_id == parent_id).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈夐儴闂ㄦ暟閲?        
        Returns:
            int: 閮ㄩ棬鏁伴噺
        """
        return self.db.query(Department).count()
    
    def exists_by_code(self, code: str) -> bool:
        """
        妫€鏌ラ儴闂ㄧ紪鐮佹槸鍚﹀瓨鍦?        
        Args:
            code: 閮ㄩ棬缂栫爜
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Department).filter(Department.code == code).first() is not None
    
    def exists_by_name_in_tenant(self, name: str, tenant_id: str) -> bool:
        """
        妫€鏌ョ鎴峰唴閮ㄩ棬鍚嶇О鏄惁瀛樺湪
        
        Args:
            name: 閮ㄩ棬鍚嶇О
            tenant_id: 绉熸埛ID
        
        Returns:
            bool: 鏄惁瀛樺湪
        """
        return self.db.query(Department).filter(
            and_(
                Department.name == name,
                Department.tenant_id == tenant_id
            )
        ).first() is not None
