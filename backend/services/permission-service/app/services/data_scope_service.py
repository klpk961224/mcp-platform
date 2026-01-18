# -*- coding: utf-8 -*-
"""
鏁版嵁鑼冨洿鏉冮檺鏈嶅姟

鍔熻兘璇存槑锛?1. 鏁版嵁鑼冨洿CRUD鎿嶄綔
2. 鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺閰嶇疆
3. 鏁版嵁鑼冨洿鏉冮檺妫€鏌?
浣跨敤绀轰緥锛?    from app.services.data_scope_service import DataScopeService
    
    data_scope_service = DataScopeService(db)
    # 妫€鏌ョ敤鎴锋槸鍚︽湁鏉冮檺璁块棶閮ㄩ棬鏁版嵁
    has_access = data_scope_service.check_data_scope("user_001", "department", "dept_001")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List

from common.database.models.data_scope import DataScope, UserDataScope
from app.repositories.data_scope_repository import DataScopeRepository, UserDataScopeRepository


class DataScopeService:
    """
    鏁版嵁鑼冨洿鏉冮檺鏈嶅姟
    
    鍔熻兘锛?    - 鏁版嵁鑼冨洿CRUD鎿嶄綔
    - 鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺閰嶇疆
    - 鏁版嵁鑼冨洿鏉冮檺妫€鏌?    
    浣跨敤鏂规硶锛?        data_scope_service = DataScopeService(db)
        has_access = data_scope_service.check_data_scope("user_001", "department", "dept_001")
    """
    
    # 鏁版嵁鑼冨洿类型甯搁噺
    DATA_SCOPE_ALL = "all"  # 鍏ㄩ儴鏁版嵁
    DATA_SCOPE_DEPARTMENT = "department"  # 鏈儴闂ㄦ暟鎹?    DATA_SCOPE_DEPARTMENT_AND_BELOW = "department_and_below"  # 鏈儴闂ㄥ強浠ヤ笅鏁版嵁
    DATA_SCOPE_SELF = "self"  # 浠呮湰浜烘暟鎹?    
    def __init__(self, db: Session):
        """
        鍒濆鍖栨暟鎹寖鍥存潈闄愭湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.data_scope_repo = DataScopeRepository(db)
        self.user_data_scope_repo = UserDataScopeRepository(db)
    
    def create_data_scope(self, data_scope_data: Dict[str, Any]) -> DataScope:
        """
        创建鏁版嵁鑼冨洿
        
        Args:
            data_scope_data: 鏁版嵁鑼冨洿鏁版嵁
        
        Returns:
            DataScope: 创建鐨勬暟鎹寖鍥村璞?        
        Raises:
            ValueError: 鏁版嵁鑼冨洿编码宸插瓨鍦?        """
        logger.info(f"创建鏁版嵁鑼冨洿: name={data_scope_data.get('name')}, code={data_scope_data.get('code')}")
        
        # 妫€鏌ユ暟鎹寖鍥寸紪鐮佹槸鍚﹀凡瀛樺湪
        if self.data_scope_repo.exists_by_code(data_scope_data.get("code")):
            raise ValueError("鏁版嵁鑼冨洿编码宸插瓨鍦?)
        
        # 创建鏁版嵁鑼冨洿
        data_scope = DataScope(**data_scope_data)
        return self.data_scope_repo.create(data_scope)
    
    def get_data_scope(self, data_scope_id: str) -> Optional[DataScope]:
        """
        鑾峰彇鏁版嵁鑼冨洿
        
        Args:
            data_scope_id: 鏁版嵁鑼冨洿ID
        
        Returns:
            Optional[DataScope]: 鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.data_scope_repo.get_by_id(data_scope_id)
    
    def get_data_scope_by_code(self, code: str) -> Optional[DataScope]:
        """
        根据编码鑾峰彇鏁版嵁鑼冨洿
        
        Args:
            code: 鏁版嵁鑼冨洿编码
        
        Returns:
            Optional[DataScope]: 鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.data_scope_repo.get_by_code(code)
    
    def list_data_scopes(self, page: int = 1, page_size: int = 10) -> List[DataScope]:
        """
        鑾峰彇鏁版嵁鑼冨洿鍒楄〃
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[DataScope]: 鏁版嵁鑼冨洿鍒楄〃
        """
        return self.data_scope_repo.get_all(page, page_size)
    
    def set_user_data_scope(self, user_id: str, module: str, data_scope_code: str) -> UserDataScope:
        """
        璁剧疆鐢ㄦ埛鐨勬暟鎹寖鍥存潈闄?        
        Args:
            user_id: 用户ID
            module: 妯″潡
            data_scope_code: 鏁版嵁鑼冨洿编码
        
        Returns:
            UserDataScope: 创建鐨勭敤鎴锋暟鎹寖鍥村璞?        
        Raises:
            ValueError: 鏁版嵁鑼冨洿涓嶅瓨鍦?        """
        logger.info(f"璁剧疆鐢ㄦ埛鏁版嵁鑼冨洿: user_id={user_id}, module={module}, data_scope_code={data_scope_code}")
        
        # 鑾峰彇鏁版嵁鑼冨洿
        data_scope = self.data_scope_repo.get_by_code(data_scope_code)
        if not data_scope:
            raise ValueError("鏁版嵁鑼冨洿涓嶅瓨鍦?)
        
        # 妫€鏌ユ槸鍚﹀凡瀛樺湪
        existing = self.user_data_scope_repo.get_by_user_module(user_id, module)
        if existing:
            # 更新
            existing.data_scope_id = data_scope.id
            return self.user_data_scope_repo.update(existing)
        else:
            # 创建
            user_data_scope = UserDataScope(
                user_id=user_id,
                module=module,
                data_scope_id=data_scope.id
            )
            return self.user_data_scope_repo.create(user_data_scope)
    
    def get_user_data_scope(self, user_id: str, module: str) -> Optional[UserDataScope]:
        """
        鑾峰彇鐢ㄦ埛鐨勬暟鎹寖鍥存潈闄?        
        Args:
            user_id: 用户ID
            module: 妯″潡
        
        Returns:
            Optional[UserDataScope]: 鐢ㄦ埛鏁版嵁鑼冨洿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.user_data_scope_repo.get_by_user_module(user_id, module)
    
    def check_data_scope(self, user_id: str, module: str, target_id: str, user_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        妫€鏌ョ敤鎴锋槸鍚︽湁鏉冮檺璁块棶鐩爣鏁版嵁
        
        Args:
            user_id: 用户ID
            module: 妯″潡
            target_id: 鐩爣鏁版嵁ID
            user_info: 鐢ㄦ埛淇℃伅锛堝寘鍚玠epartment_id绛夛級
        
        Returns:
            bool: 鏄惁鏈夋潈闄?        """
        logger.debug(f"妫€鏌ユ暟鎹寖鍥存潈闄? user_id={user_id}, module={module}, target_id={target_id}")
        
        # 鑾峰彇鐢ㄦ埛鐨勬暟鎹寖鍥?        user_data_scope = self.get_user_data_scope(user_id, module)
        if not user_data_scope:
            # 默认涓轰粎鏈汉鏁版嵁
            data_scope_code = self.DATA_SCOPE_SELF
        else:
            data_scope_code = user_data_scope.data_scope.code
        
        # 根据鏁版嵁鑼冨洿类型妫€鏌ユ潈闄?        if data_scope_code == self.DATA_SCOPE_ALL:
            # 鍏ㄩ儴鏁版嵁锛氭湁鏉冮檺
            return True
        elif data_scope_code == self.DATA_SCOPE_DEPARTMENT:
            # 鏈儴闂ㄦ暟鎹細妫€鏌ユ槸鍚﹀睘浜庡悓涓€閮ㄩ棬
            if not user_info:
                return False
            user_department_id = user_info.get("department_id")
            if not user_department_id:
                return False
            return self._check_same_department(target_id, user_department_id, module)
        elif data_scope_code == self.DATA_SCOPE_DEPARTMENT_AND_BELOW:
            # 鏈儴闂ㄥ強浠ヤ笅鏁版嵁锛氭鏌ユ槸鍚﹀睘浜庢湰閮ㄩ棬鎴栧瓙閮ㄩ棬
            if not user_info:
                return False
            user_department_id = user_info.get("department_id")
            if not user_department_id:
                return False
            return self._check_department_and_below(target_id, user_department_id, module)
        elif data_scope_code == self.DATA_SCOPE_SELF:
            # 浠呮湰浜烘暟鎹細妫€鏌ユ槸鍚︽槸鏈汉
            return target_id == user_id
        else:
            # 鏈煡鏁版嵁鑼冨洿类型锛氶粯璁ゆ棤鏉冮檺
            return False
    
    def _check_same_department(self, target_id: str, user_department_id: str, module: str) -> bool:
        """
        妫€鏌ョ洰鏍囨槸鍚﹀睘浜庡悓涓€閮ㄩ棬
        
        Args:
            target_id: 鐩爣ID
            user_department_id: 鐢ㄦ埛部门ID
            module: 妯″潡
        
        Returns:
            bool: 鏄惁灞炰簬鍚屼竴閮ㄩ棬
        """
        # 根据妯″潡查询鐩爣鏁版嵁鐨勯儴闂↖D
        target_department_id = self._get_target_department_id(target_id, module)
        if not target_department_id:
            return False
        return target_department_id == user_department_id
    
    def _check_department_and_below(self, target_id: str, user_department_id: str, module: str) -> bool:
        """
        妫€鏌ョ洰鏍囨槸鍚﹀睘浜庢湰閮ㄩ棬鎴栧瓙閮ㄩ棬
        
        Args:
            target_id: 鐩爣ID
            user_department_id: 鐢ㄦ埛部门ID
            module: 妯″潡
        
        Returns:
            bool: 鏄惁灞炰簬鏈儴闂ㄦ垨瀛愰儴闂?        """
        # 根据妯″潡查询鐩爣鏁版嵁鐨勯儴闂↖D
        target_department_id = self._get_target_department_id(target_id, module)
        if not target_department_id:
            return False
        
        # 濡傛灉鏄悓涓€閮ㄩ棬锛屾湁鏉冮檺
        if target_department_id == user_department_id:
            return True
        
        # 妫€鏌ユ槸鍚︽槸瀛愰儴闂?        return self._is_child_department(target_department_id, user_department_id)
    
    def _is_child_department(self, child_id: str, parent_id: str) -> bool:
        """
        妫€鏌ユ槸鍚︽槸瀛愰儴闂?        
        Args:
            child_id: 瀛愰儴闂↖D
            parent_id: 鐖堕儴闂↖D
        
        Returns:
            bool: 鏄惁鏄瓙閮ㄩ棬
        """
        from common.database.models.user import Department
        
        # 鑾峰彇鐖堕儴闂ㄧ殑鎵€鏈夊瓙閮ㄩ棬
        child_departments = self.db.query(Department).filter(
            Department.parent_id == parent_id
        ).all()
        
        # 妫€鏌ユ槸鍚︽槸鐩存帴瀛愰儴闂?        if any(dept.id == child_id for dept in child_departments):
            return True
        
        # 閫掑綊妫€鏌ュ瓙閮ㄩ棬鐨勫瓙閮ㄩ棬
        for dept in child_departments:
            if self._is_child_department(child_id, dept.id):
                return True
        
        return False
    
    def _get_target_department_id(self, target_id: str, module: str) -> Optional[str]:
        """
        鑾峰彇鐩爣鏁版嵁鐨勯儴闂↖D
        
        Args:
            target_id: 鐩爣ID
            module: 妯″潡
        
        Returns:
            Optional[str]: 部门ID
        """
        if module == "user":
            # 查询鐢ㄦ埛鐨勯儴闂↖D
            from common.database.models.user import User
            user = self.db.query(User).filter(User.id == target_id).first()
            return user.department_id if user else None
        elif module == "department":
            # 查询閮ㄩ棬鐨勭埗部门ID
            from common.database.models.user import Department
            department = self.db.query(Department).filter(Department.id == target_id).first()
            return department.parent_id if department else None
        else:
            return None
