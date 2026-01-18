# -*- coding: utf-8 -*-
"""
閮ㄩ棬涓氬姟閫昏緫灞?
鍔熻兘璇存槑锛?1. 閮ㄩ棬CRUD鎿嶄綔
2. 閮ㄩ棬鏍戝舰缁撴瀯绠＄悊
3. 閮ㄩ棬灞傜骇鑷姩璁＄畻
4. 部门编码鑷姩鐢熸垚
5. 閮ㄩ棬删除楠岃瘉

浣跨敤绀轰緥锛?    from app.services.department_service import DepartmentService
    
    dept_service = DepartmentService(db)
    dept = dept_service.create_department({
        "name": "鎶€鏈儴",
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
    閮ㄩ棬涓氬姟閫昏緫灞?    
    鍔熻兘锛?    - 閮ㄩ棬CRUD鎿嶄綔
    - 閮ㄩ棬鏍戝舰缁撴瀯绠＄悊
    - 閮ㄩ棬灞傜骇鑷姩璁＄畻
    - 部门编码鑷姩鐢熸垚
    - 閮ㄩ棬删除楠岃瘉
    
    浣跨敤鏂规硶锛?        dept_service = DepartmentService(db)
        dept = dept_service.create_department({
            "name": "鎶€鏈儴",
            "tenant_id": "tenant_001"
        })
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栭儴闂ㄤ笟鍔￠€昏緫灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.dept_repo = DepartmentRepository(db)
    
    def create_department(self, dept_data: Dict) -> Department:
        """
        创建閮ㄩ棬
        
        鍔熻兘锛?        - 楠岃瘉部门编码鍞竴鎬?        - 楠岃瘉部门名称鍦ㄧ鎴峰唴鍞竴鎬?        - 鑷姩璁＄畻閮ㄩ棬灞傜骇
        - 鑷姩鐢熸垚部门编码锛堝鏋滄湭鎻愪緵锛?        
        Args:
            dept_data: 閮ㄩ棬鏁版嵁
                - name: 部门名称锛堝繀濉級
                - code: 部门编码锛堝彲閫夛紝鑷姩鐢熸垚锛?                - tenant_id: 租户ID锛堝繀濉級
                - parent_id: 鐖堕儴闂↖D锛堝彲閫夛級
                - level: 灞傜骇锛堝彲閫夛紝鑷姩璁＄畻锛?                - sort_order: 排序锛堝彲閫夛級
                - description: 描述锛堝彲閫夛級
                - leader_id: 璐熻矗浜篒D锛堝彲閫夛級
                - phone: 鑱旂郴鐢佃瘽锛堝彲閫夛級
                - email: 鑱旂郴邮箱锛堝彲閫夛級
        
        Returns:
            Department: 创建鐨勯儴闂ㄥ璞?        
        Raises:
            ValueError: 部门编码宸插瓨鍦ㄦ垨部门名称宸插瓨鍦?        """
        logger.info(f"创建閮ㄩ棬: name={dept_data.get('name')}, tenant_id={dept_data.get('tenant_id')}")
        
        # 楠岃瘉必填瀛楁
        if not dept_data.get('name'):
            raise ValueError("部门名称涓嶈兘涓虹┖")
        
        if not dept_data.get('tenant_id'):
            raise ValueError("租户ID涓嶈兘涓虹┖")
        
        # 妫€鏌ラ儴闂ㄧ紪鐮佹槸鍚﹀瓨鍦?        code = dept_data.get('code')
        if code and self.dept_repo.exists_by_code(code):
            raise ValueError(f"部门编码宸插瓨鍦? {code}")
        
        # 妫€鏌ラ儴闂ㄥ悕绉板湪绉熸埛鍐呮槸鍚﹀瓨鍦?        if self.dept_repo.exists_by_name_in_tenant(dept_data['name'], dept_data['tenant_id']):
            raise ValueError(f"部门名称宸插瓨鍦? {dept_data['name']}")
        
        # 鑷姩鐢熸垚部门编码
        if not code:
            code = self._generate_code(dept_data['tenant_id'], dept_data.get('parent_id'))
            dept_data['code'] = code
        
        # 鑷姩璁＄畻閮ㄩ棬灞傜骇
        parent_id = dept_data.get('parent_id')
        if parent_id:
            parent = self.dept_repo.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"鐖堕儴闂ㄤ笉瀛樺湪: {parent_id}")
            if parent.tenant_id != dept_data['tenant_id']:
                raise ValueError("鐖堕儴闂ㄤ笌褰撳墠閮ㄩ棬涓嶅湪鍚屼竴绉熸埛")
            dept_data['level'] = parent.level + 1
        else:
            dept_data['level'] = 1
        
        # 创建閮ㄩ棬
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
        鑾峰彇閮ㄩ棬璇︽儏
        
        Args:
            department_id: 部门ID
        
        Returns:
            Optional[Department]: 閮ㄩ棬瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.dept_repo.get_by_id(department_id)
    
    def update_department(self, department_id: str, dept_data: Dict) -> Department:
        """
        更新閮ㄩ棬
        
        鍔熻兘锛?        - 楠岃瘉部门编码鍞竴鎬э紙濡傛灉淇敼浜嗙紪鐮侊級
        - 楠岃瘉部门名称鍦ㄧ鎴峰唴鍞竴鎬э紙濡傛灉淇敼浜嗗悕绉帮級
        - 鑷姩璁＄畻閮ㄩ棬灞傜骇锛堝鏋滀慨鏀逛簡鐖堕儴闂級
        
        Args:
            department_id: 部门ID
            dept_data: 閮ㄩ棬鏁版嵁
        
        Returns:
            Department: 更新鍚庣殑閮ㄩ棬瀵硅薄
        
        Raises:
            ValueError: 閮ㄩ棬涓嶅瓨鍦ㄦ垨楠岃瘉澶辫触
        """
        logger.info(f"更新閮ㄩ棬: department_id={department_id}")
        
        # 鑾峰彇閮ㄩ棬
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise ValueError(f"閮ㄩ棬涓嶅瓨鍦? {department_id}")
        
        # 更新部门名称
        if dept_data.get('name') and dept_data['name'] != department.name:
            # 妫€鏌ラ儴闂ㄥ悕绉板湪绉熸埛鍐呮槸鍚﹀瓨鍦?            if self.dept_repo.exists_by_name_in_tenant(dept_data['name'], department.tenant_id):
                raise ValueError(f"部门名称宸插瓨鍦? {dept_data['name']}")
            department.name = dept_data['name']
        
        # 更新部门编码
        if dept_data.get('code') and dept_data['code'] != department.code:
            # 妫€鏌ラ儴闂ㄧ紪鐮佹槸鍚﹀瓨鍦?            if self.dept_repo.exists_by_code(dept_data['code']):
                raise ValueError(f"部门编码宸插瓨鍦? {dept_data['code']}")
            department.code = dept_data['code']
        
        # 更新鐖堕儴闂?        if dept_data.get('parent_id') != department.parent_id:
            new_parent_id = dept_data.get('parent_id')
            
            # 妫€鏌ユ槸鍚﹀皢閮ㄩ棬璁剧疆涓鸿嚜宸辩殑瀛愰儴闂?            if new_parent_id:
                if self._is_descendant(department_id, new_parent_id):
                    raise ValueError("涓嶈兘灏嗛儴闂ㄨ缃负鑷繁鐨勫瓙閮ㄩ棬")
                
                parent = self.dept_repo.get_by_id(new_parent_id)
                if not parent:
                    raise ValueError(f"鐖堕儴闂ㄤ笉瀛樺湪: {new_parent_id}")
                if parent.tenant_id != department.tenant_id:
                    raise ValueError("鐖堕儴闂ㄤ笌褰撳墠閮ㄩ棬涓嶅湪鍚屼竴绉熸埛")
                
                department.parent_id = new_parent_id
                department.level = parent.level + 1
            else:
                department.parent_id = None
                department.level = 1
            
            # 更新鎵€鏈夊瓙閮ㄩ棬鐨勫眰绾?            self._update_children_level(department_id)
        
        # 更新鍏朵粬瀛楁
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
        删除閮ㄩ棬
        
        鍔熻兘锛?        - 妫€鏌ラ儴闂ㄦ槸鍚﹀瓨鍦?        - 妫€鏌ユ槸鍚︽湁瀛愰儴闂?        - 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        
        Args:
            department_id: 部门ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        
        Raises:
            ValueError: 閮ㄩ棬涓嶅瓨鍦ㄦ垨鏈夊瓙閮ㄩ棬鎴栨湁鐢ㄦ埛
        """
        logger.info(f"删除閮ㄩ棬: department_id={department_id}")
        
        # 鑾峰彇閮ㄩ棬
        department = self.dept_repo.get_by_id(department_id)
        if not department:
            raise ValueError(f"閮ㄩ棬涓嶅瓨鍦? {department_id}")
        
        # 妫€鏌ユ槸鍚︽湁瀛愰儴闂?        if department.children:
            raise ValueError("鏃犳硶删除閮ㄩ棬锛氳閮ㄩ棬涓嬪瓨鍦ㄥ瓙閮ㄩ棬")
        
        # 妫€鏌ユ槸鍚︽湁鐢ㄦ埛
        if department.users:
            raise ValueError("鏃犳硶删除閮ㄩ棬锛氳閮ㄩ棬涓嬪瓨鍦ㄧ敤鎴?)
        
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
        鑾峰彇閮ㄩ棬鍒楄〃
        
        Args:
            tenant_id: 租户ID锛堝彲閫夛級
            parent_id: 鐖堕儴闂↖D锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            Dict: 閮ㄩ棬鍒楄〃
                - total: 鎬绘暟
                - items: 閮ㄩ棬鍒楄〃
                - page: 椤电爜
                - page_size: 姣忛〉数量
        """
        # 根据鏉′欢查询
        if keyword:
            departments = self.dept_repo.search(keyword, tenant_id, page, page_size)
            total = len(departments)  # TODO: 闇€瑕佷紭鍖栵紝搴旇鍗曠嫭查询鎬绘暟
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
        鑾峰彇閮ㄩ棬鏍?        
        Args:
            tenant_id: 租户ID
        
        Returns:
            List[Dict]: 閮ㄩ棬鏍?        """
        root_departments = self.dept_repo.get_tree(tenant_id)
        return [dept.to_tree_dict() for dept in root_departments]
    
    def _generate_code(self, tenant_id: str, parent_id: Optional[str] = None) -> str:
        """
        鑷姩鐢熸垚部门编码
        
        瑙勫垯锛?        - 鏍归儴闂細DEPT_{租户ID}_{搴忓彿}
        - 瀛愰儴闂細{鐖堕儴闂ㄧ紪鐮亇_{搴忓彿}
        
        Args:
            tenant_id: 租户ID
            parent_id: 鐖堕儴闂↖D
        
        Returns:
            str: 部门编码
        """
        if parent_id:
            # 瀛愰儴闂ㄧ紪鐮?            parent = self.dept_repo.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"鐖堕儴闂ㄤ笉瀛樺湪: {parent_id}")
            
            # 鑾峰彇鍚岀骇閮ㄩ棬数量
            siblings_count = self.dept_repo.count_by_parent(parent_id)
            code = f"{parent.code}_{siblings_count + 1:03d}"
        else:
            # 鏍归儴闂ㄧ紪鐮?            root_count = self.dept_repo.count_by_tenant(tenant_id)
            code = f"DEPT_{tenant_id}_{root_count + 1:03d}"
        
        # 妫€鏌ョ紪鐮佹槸鍚﹀凡瀛樺湪
        if self.dept_repo.exists_by_code(code):
            # 濡傛灉宸插瓨鍦紝閫掑綊鐢熸垚鏂扮殑编码
            return self._generate_code(tenant_id, parent_id)
        
        return code
    
    def _is_descendant(self, department_id: str, child_id: str) -> bool:
        """
        妫€鏌hild_id鏄惁鏄痙epartment_id鐨勫瓙瀛欓儴闂?        
        Args:
            department_id: 部门ID
            child_id: 瀛愰儴闂↖D
        
        Returns:
            bool: 鏄惁鏄瓙瀛欓儴闂?        """
        if department_id == child_id:
            return True
        
        child = self.dept_repo.get_by_id(child_id)
        if not child or not child.parent_id:
            return False
        
        return self._is_descendant(department_id, child.parent_id)
    
    def _update_children_level(self, department_id: str):
        """
        閫掑綊更新瀛愰儴闂ㄧ殑灞傜骇
        
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
