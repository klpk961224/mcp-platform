# -*- coding: utf-8 -*-
"""
寰呭姙浠诲姟鏈嶅姟

鍔熻兘璇存槑锛?1. 寰呭姙浠诲姟绠＄悊
2. 姣忔棩璁″垝绠＄悊
3. 浠诲姟鎻愰啋

浣跨敤绀轰緥锛?    from app.services.todo_service import TodoService
    
    todo_service = TodoService(db)
    todo = todo_service.create_todo(title="瀹屾垚鏂囨。", description="...")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
from datetime import datetime, date, timedelta

from app.models.todo import TodoTask, DailyPlan
from app.repositories.todo_repository import TodoRepository
from app.services.notification_service import NotificationService


class TodoService:
    """
    寰呭姙浠诲姟鏈嶅姟
    
    鍔熻兘锛?    - 寰呭姙浠诲姟绠＄悊
    - 姣忔棩璁″垝绠＄悊
    - 浠诲姟鎻愰啋
    
    浣跨敤鏂规硶锛?        todo_service = TodoService(db)
        todo = todo_service.create_todo(title="瀹屾垚鏂囨。", description="...")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧緟鍔炰换鍔℃湇鍔?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.todo_repo = TodoRepository(db)
        self.notification_service = NotificationService(db)
    
    def create_todo(self, title: str, user_id: str, tenant_id: str,
                    description: Optional[str] = None, task_type: str = "personal",
                    priority: str = "medium", due_date: Optional[datetime] = None,
                    due_time: Optional[str] = None, tags: Optional[List[str]] = None,
                    attachment: Optional[str] = None) -> TodoTask:
        """
        鍒涘缓寰呭姙浠诲姟
        
        Args:
            title: 浠诲姟鏍囬
            user_id: 鐢ㄦ埛ID
            tenant_id: 绉熸埛ID
            description: 浠诲姟鎻忚堪锛堝彲閫夛級
            task_type: 浠诲姟绫诲瀷
            priority: 浼樺厛绾?            due_date: 鎴鏃ユ湡锛堝彲閫夛級
            due_time: 鎴鏃堕棿锛堝彲閫夛級
            tags: 鏍囩鍒楄〃锛堝彲閫夛級
            attachment: 闄勪欢URL锛堝彲閫夛級
        
        Returns:
            TodoTask: 鍒涘缓鐨勫緟鍔炰换鍔″璞?        """
        logger.info(f"鍒涘缓寰呭姙浠诲姟: title={title}, user_id={user_id}")
        
        todo = TodoTask(
            tenant_id=tenant_id,
            user_id=user_id,
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            status="pending",
            due_date=due_date
        )
        
        return self.todo_repo.create_todo(todo)
    
    def get_todo(self, todo_id: str) -> Optional[TodoTask]:
        """
        鑾峰彇寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
        
        Returns:
            Optional[TodoTask]: 寰呭姙浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.todo_repo.get_todo_by_id(todo_id)
    
    def update_todo(self, todo_id: str, todo_data: Dict[str, Any]) -> Optional[TodoTask]:
        """
        鏇存柊寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
            todo_data: 鏇存柊鏁版嵁
        
        Returns:
            Optional[TodoTask]: 鏇存柊鍚庣殑浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鏇存柊寰呭姙浠诲姟: todo_id={todo_id}")
        
        todo = self.todo_repo.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        # 鏇存柊浠诲姟
        for key, value in todo_data.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        
        return self.todo_repo.update_todo(todo)
    
    def get_user_todos(self, user_id: str, status: Optional[str] = None,
                       priority: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        鑾峰彇鐢ㄦ埛寰呭姙浠诲姟
        
        Args:
            user_id: 鐢ㄦ埛ID
            status: 鐘舵€侊紙鍙€夛級
            priority: 浼樺厛绾э紙鍙€夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[TodoTask]: 寰呭姙浠诲姟鍒楄〃
        """
        return self.todo_repo.get_user_todos(user_id, status, priority, page, page_size)
    
    def list_todos(self, user_id: str, status: Optional[str] = None,
                   task_type: Optional[str] = None, priority: Optional[str] = None,
                   is_overdue: Optional[bool] = None, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        鑾峰彇寰呭姙浠诲姟鍒楄〃
        
        Args:
            user_id: 鐢ㄦ埛ID
            status: 鐘舵€侊紙鍙€夛級
            task_type: 浠诲姟绫诲瀷锛堝彲閫夛級
            priority: 浼樺厛绾э紙鍙€夛級
            is_overdue: 鏄惁閫炬湡锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[TodoTask]: 寰呭姙浠诲姟鍒楄〃
        """
        if is_overdue is not None:
            return self.todo_repo.get_overdue_todos(page, page_size)
        else:
            return self.todo_repo.get_user_todos(user_id, status, priority, page, page_size)
    
    def complete_todo(self, todo_id: str) -> Optional[TodoTask]:
        """
        瀹屾垚寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
        
        Returns:
            Optional[TodoTask]: 鏇存柊鍚庣殑浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"瀹屾垚寰呭姙浠诲姟: todo_id={todo_id}")
        
        todo = self.todo_repo.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        todo.mark_completed()
        return self.todo_repo.update_todo(todo)
    
    def uncomplete_todo(self, todo_id: str) -> Optional[TodoTask]:
        """
        鍙栨秷瀹屾垚寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
        
        Returns:
            Optional[TodoTask]: 鏇存柊鍚庣殑浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鍙栨秷瀹屾垚寰呭姙浠诲姟: todo_id={todo_id}")
        
        todo = self.todo_repo.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        todo.mark_pending()
        return self.todo_repo.update_todo(todo)
    
    def delete_todo(self, todo_id: str) -> bool:
        """
        鍒犻櫎寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎寰呭姙浠诲姟: todo_id={todo_id}")
        return self.todo_repo.delete_todo(todo_id)
    
    def get_overdue_todos(self, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        鑾峰彇閫炬湡浠诲姟
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[TodoTask]: 閫炬湡浠诲姟鍒楄〃
        """
        return self.todo_repo.get_overdue_todos(page, page_size)
    
    def update_overdue_status(self):
        """
        鏇存柊鎵€鏈変换鍔＄殑閫炬湡鐘舵€?        """
        logger.info("鏇存柊鎵€鏈変换鍔＄殑閫炬湡鐘舵€?)
        
        todos = self.todo_repo.get_tenant_todos(tenant_id=None, page=1, page_size=10000)
        for todo in todos:
            todo.update_overdue_status()
            self.todo_repo.update_todo(todo)
    
    def create_daily_plan(self, user_id: str, tenant_id: str, plan_date: date,
                          tasks: List[Dict[str, Any]], notes: Optional[str] = None) -> DailyPlan:
        """
        鍒涘缓姣忔棩璁″垝
        
        Args:
            user_id: 鐢ㄦ埛ID
            tenant_id: 绉熸埛ID
            plan_date: 璁″垝鏃ユ湡
            tasks: 浠诲姟鍒楄〃
            notes: 澶囨敞锛堝彲閫夛級
        
        Returns:
            DailyPlan: 鍒涘缓鐨勬瘡鏃ヨ鍒掑璞?        """
        logger.info(f"鍒涘缓姣忔棩璁″垝: user_id={user_id}, plan_date={plan_date}")
        
        daily_plan = DailyPlan(
            tenant_id=tenant_id,
            user_id=user_id,
            plan_date=datetime.combine(plan_date, datetime.min.time()),
            status='active'
        )
        
        return self.todo_repo.create_daily_plan(daily_plan)
    
    def get_user_daily_plan(self, user_id: str, plan_date: date) -> Optional[DailyPlan]:
        """
        鑾峰彇鐢ㄦ埛鎸囧畾鏃ユ湡鐨勬瘡鏃ヨ鍒?        
        Args:
            user_id: 鐢ㄦ埛ID
            plan_date: 璁″垝鏃ユ湡
        
        Returns:
            Optional[DailyPlan]: 姣忔棩璁″垝瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.todo_repo.get_user_daily_plan(user_id, plan_date)
    
    def get_todo_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        鑾峰彇鐢ㄦ埛寰呭姙浠诲姟缁熻淇℃伅
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            Dict[str, Any]: 缁熻淇℃伅
        """
        return self.todo_repo.get_todo_statistics(user_id)
    
    def send_overdue_reminders(self):
        """
        鍙戦€侀€炬湡浠诲姟鎻愰啋
        """
        logger.info("鍙戦€侀€炬湡浠诲姟鎻愰啋")
        
        overdue_todos = self.todo_repo.get_overdue_todos(page=1, page_size=1000)
        for todo in overdue_todos:
            if not todo.reminder_sent:
                # 鍙戦€佹彁閱掗€氱煡
                self.notification_service.send_system_notification(
                    title="浠诲姟閫炬湡鎻愰啋",
                    content=f"鎮ㄧ殑浠诲姟銆寋todo.title}銆嶅凡閫炬湡锛岃灏藉揩澶勭悊锛?,
                    tenant_id=todo.tenant_id,
                    target_ids=[todo.user_id],
                    priority="high"
                )
                
                # 鏍囪涓哄凡鍙戦€?                todo.reminder_sent = True
                self.todo_repo.update_todo(todo)
    
    def send_due_date_reminders(self, hours_before: int = 24):
        """
        鍙戦€佸嵆灏嗗埌鏈熶换鍔℃彁閱?        
        Args:
            hours_before: 鎻愬墠灏忔椂鏁?        """
        logger.info(f"鍙戦€佸嵆灏嗗埌鏈熶换鍔℃彁閱掞紙鎻愬墠{hours_before}灏忔椂锛?)
        
        threshold_time = datetime.now() + timedelta(hours=hours_before)
        
        # 鑾峰彇鎵€鏈夋湭瀹屾垚鐨勪换鍔?        all_todos = self.todo_repo.get_tenant_todos(tenant_id=None, page=1, page_size=10000)
        for todo in all_todos:
            if todo.due_date and todo.status != 'completed':
                # 妫€鏌ユ槸鍚﹀湪鎻愰啋鏃堕棿鑼冨洿鍐?                time_diff = (todo.due_date - datetime.now()).total_seconds()
                if 0 < time_diff <= hours_before * 3600:
                    # 鍙戦€佹彁閱掗€氱煡
                    self.notification_service.send_system_notification(
                        title="浠诲姟鍗冲皢鍒版湡",
                        content=f"鎮ㄧ殑浠诲姟銆寋todo.title}銆嶅皢浜巤todo.due_date.strftime('%Y-%m-%d %H:%M')}鍒版湡锛岃鍙婃椂澶勭悊锛?,
                        tenant_id=todo.tenant_id,
                        target_ids=[todo.user_id],
                        priority="medium"
                    )
    
    def count_todos(self, user_id: Optional[str] = None, status: Optional[str] = None) -> int:
        """
        缁熻寰呭姙浠诲姟鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID锛堝彲閫夛級
            status: 鐘舵€侊紙鍙€夛級
        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        if user_id:
            return self.todo_repo.count_todos_by_user(user_id, status)
        else:
            return self.todo_repo.count_all_todos()
