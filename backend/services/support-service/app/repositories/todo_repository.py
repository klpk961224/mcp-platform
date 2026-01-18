# -*- coding: utf-8 -*-
"""
寰呭姙浠诲姟鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. 寰呭姙浠诲姟CRUD鎿嶄綔
2. 姣忔棩璁″垝CRUD鎿嶄綔
3. 寰呭姙浠诲姟鏌ヨ鍜岀粺璁?
浣跨敤绀轰緥锛?    from app.repositories.todo_repository import TodoRepository
    
    todo_repo = TodoRepository(db)
    todos = todo_repo.get_user_todos(user_id="123")
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import Optional, List
from loguru import logger
from datetime import datetime, date

from app.models.todo import TodoTask, DailyPlan


class TodoRepository:
    """
    寰呭姙浠诲姟鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - 寰呭姙浠诲姟CRUD鎿嶄綔
    - 姣忔棩璁″垝CRUD鎿嶄綔
    - 寰呭姙浠诲姟鏌ヨ鍜岀粺璁?    
    浣跨敤鏂规硶锛?        todo_repo = TodoRepository(db)
        todos = todo_repo.get_user_todos(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖栧緟鍔炰换鍔℃暟鎹闂眰
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    # 寰呭姙浠诲姟鐩稿叧鏂规硶
    def create_todo(self, todo: TodoTask) -> TodoTask:
        """
        鍒涘缓寰呭姙浠诲姟
        
        Args:
            todo: 寰呭姙浠诲姟瀵硅薄
        
        Returns:
            TodoTask: 鍒涘缓鐨勫緟鍔炰换鍔″璞?        """
        logger.info(f"鍒涘缓寰呭姙浠诲姟: title={todo.title}, user_id={todo.user_id}")
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def get_todo_by_id(self, todo_id: str) -> Optional[TodoTask]:
        """
        鏍规嵁ID鑾峰彇寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
        
        Returns:
            Optional[TodoTask]: 寰呭姙浠诲姟瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(TodoTask).filter(TodoTask.id == todo_id).first()
    
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
        offset = (page - 1) * page_size
        query = self.db.query(TodoTask).filter(TodoTask.user_id == user_id)
        
        if status:
            query = query.filter(TodoTask.status == status)
        if priority:
            query = query.filter(TodoTask.priority == priority)
        
        return query.order_by(TodoTask.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_tenant_todos(self, tenant_id: str, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        鑾峰彇绉熸埛寰呭姙浠诲姟
        
        Args:
            tenant_id: 绉熸埛ID
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[TodoTask]: 寰呭姙浠诲姟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(TodoTask).filter(
            TodoTask.tenant_id == tenant_id
        ).order_by(TodoTask.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_overdue_todos(self, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        鑾峰彇閫炬湡浠诲姟
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[TodoTask]: 閫炬湡浠诲姟鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(TodoTask).filter(
            and_(
                TodoTask.status != "completed",
                TodoTask.due_date < datetime.now()
            )
        ).order_by(TodoTask.due_date.asc()).offset(offset).limit(page_size).all()
    
    def search_todos(self, keyword: str, tenant_id: Optional[str] = None,
                      page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        鎼滅储寰呭姙浠诲姟
        
        Args:
            keyword: 鍏抽敭璇?            tenant_id: 绉熸埛ID锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[TodoTask]: 寰呭姙浠诲姟鍒楄〃
        """
        offset = (page - 1) * page_size
        query = self.db.query(TodoTask).filter(
            or_(
                TodoTask.title.like(f"%{keyword}%"),
                TodoTask.description.like(f"%{keyword}%")
            )
        )
        
        if tenant_id:
            query = query.filter(TodoTask.tenant_id == tenant_id)
        
        return query.order_by(TodoTask.created_at.desc()).offset(offset).limit(page_size).all()
    
    def update_todo(self, todo: TodoTask) -> TodoTask:
        """
        鏇存柊寰呭姙浠诲姟
        
        Args:
            todo: 寰呭姙浠诲姟瀵硅薄
        
        Returns:
            TodoTask: 鏇存柊鍚庣殑寰呭姙浠诲姟瀵硅薄
        """
        logger.info(f"鏇存柊寰呭姙浠诲姟: todo_id={todo.id}")
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def delete_todo(self, todo_id: str) -> bool:
        """
        鍒犻櫎寰呭姙浠诲姟
        
        Args:
            todo_id: 浠诲姟ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎寰呭姙浠诲姟: todo_id={todo_id}")
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        self.db.delete(todo)
        self.db.commit()
        return True
    
    # 姣忔棩璁″垝鐩稿叧鏂规硶
    def create_daily_plan(self, daily_plan: DailyPlan) -> DailyPlan:
        """
        鍒涘缓姣忔棩璁″垝
        
        Args:
            daily_plan: 姣忔棩璁″垝瀵硅薄
        
        Returns:
            DailyPlan: 鍒涘缓鐨勬瘡鏃ヨ鍒掑璞?        """
        logger.info(f"鍒涘缓姣忔棩璁″垝: user_id={daily_plan.user_id}, plan_date={daily_plan.plan_date}")
        self.db.add(daily_plan)
        self.db.commit()
        self.db.refresh(daily_plan)
        return daily_plan
    
    def get_daily_plan_by_id(self, plan_id: str) -> Optional[DailyPlan]:
        """
        鏍规嵁ID鑾峰彇姣忔棩璁″垝
        
        Args:
            plan_id: 璁″垝ID
        
        Returns:
            Optional[DailyPlan]: 姣忔棩璁″垝瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(DailyPlan).filter(DailyPlan.id == plan_id).first()
    
    def get_user_daily_plan(self, user_id: str, plan_date: date) -> Optional[DailyPlan]:
        """
        鑾峰彇鐢ㄦ埛鎸囧畾鏃ユ湡鐨勬瘡鏃ヨ鍒?        
        Args:
            user_id: 鐢ㄦ埛ID
            plan_date: 璁″垝鏃ユ湡
        
        Returns:
            Optional[DailyPlan]: 姣忔棩璁″垝瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        start_date = datetime.combine(plan_date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        
        return self.db.query(DailyPlan).filter(
            and_(
                DailyPlan.user_id == user_id,
                DailyPlan.plan_date >= start_date,
                DailyPlan.plan_date < end_date
            )
        ).first()
    
    def get_user_daily_plans(self, user_id: str, start_date: Optional[date] = None,
                             end_date: Optional[date] = None, page: int = 1, page_size: int = 10) -> List[DailyPlan]:
        """
        鑾峰彇鐢ㄦ埛姣忔棩璁″垝鍒楄〃
        
        Args:
            user_id: 鐢ㄦ埛ID
            start_date: 寮€濮嬫棩鏈燂紙鍙€夛級
            end_date: 缁撴潫鏃ユ湡锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[DailyPlan]: 姣忔棩璁″垝鍒楄〃
        """
        offset = (page - 1) * page_size
        query = self.db.query(DailyPlan).filter(DailyPlan.user_id == user_id)
        
        if start_date:
            query = query.filter(DailyPlan.plan_date >= datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query = query.filter(DailyPlan.plan_date < datetime.combine(end_date, datetime.min.time()))
        
        return query.order_by(DailyPlan.plan_date.desc()).offset(offset).limit(page_size).all()
    
    def update_daily_plan(self, daily_plan: DailyPlan) -> DailyPlan:
        """
        鏇存柊姣忔棩璁″垝
        
        Args:
            daily_plan: 姣忔棩璁″垝瀵硅薄
        
        Returns:
            DailyPlan: 鏇存柊鍚庣殑姣忔棩璁″垝瀵硅薄
        """
        logger.info(f"鏇存柊姣忔棩璁″垝: plan_id={daily_plan.id}")
        self.db.commit()
        self.db.refresh(daily_plan)
        return daily_plan
    
    def delete_daily_plan(self, plan_id: str) -> bool:
        """
        鍒犻櫎姣忔棩璁″垝
        
        Args:
            plan_id: 璁″垝ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎姣忔棩璁″垝: plan_id={plan_id}")
        daily_plan = self.get_daily_plan_by_id(plan_id)
        if not daily_plan:
            return False
        
        self.db.delete(daily_plan)
        self.db.commit()
        return True
    
    # 缁熻鏂规硶
    def count_todos_by_user(self, user_id: str, status: Optional[str] = None) -> int:
        """
        缁熻鐢ㄦ埛寰呭姙浠诲姟鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID
            status: 鐘舵€侊紙鍙€夛級
        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        query = self.db.query(TodoTask).filter(TodoTask.user_id == user_id)
        if status:
            query = query.filter(TodoTask.status == status)
        return query.count()
    
    def count_overdue_todos(self, user_id: str) -> int:
        """
        缁熻鐢ㄦ埛閫炬湡浠诲姟鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            int: 閫炬湡浠诲姟鏁伴噺
        """
        return self.db.query(TodoTask).filter(
            and_(
                TodoTask.user_id == user_id,
                TodoTask.status != "completed",
                TodoTask.due_date < datetime.now()
            )
        ).count()
    
    def count_all_todos(self) -> int:
        """
        缁熻鎵€鏈夊緟鍔炰换鍔℃暟閲?        
        Returns:
            int: 浠诲姟鏁伴噺
        """
        return self.db.query(TodoTask).count()
    
    def get_todo_statistics(self, user_id: str) -> dict:
        """
        鑾峰彇鐢ㄦ埛寰呭姙浠诲姟缁熻淇℃伅
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            dict: 缁熻淇℃伅
        """
        total = self.count_todos_by_user(user_id)
        completed = self.count_todos_by_user(user_id, "completed")
        pending = self.count_todos_by_user(user_id, "pending")
        in_progress = self.count_todos_by_user(user_id, "in_progress")
        overdue = self.count_overdue_todos(user_id)
        
        # 鎸変紭鍏堢骇缁熻
        high_priority = self.db.query(TodoTask).filter(
            and_(
                TodoTask.user_id == user_id,
                TodoTask.priority == "high",
                TodoTask.status != "completed"
            )
        ).count()
        
        medium_priority = self.db.query(TodoTask).filter(
            and_(
                TodoTask.user_id == user_id,
                TodoTask.priority == "medium",
                TodoTask.status != "completed"
            )
        ).count()
        
        low_priority = self.db.query(TodoTask).filter(
            and_(
                TodoTask.user_id == user_id,
                TodoTask.priority == "low",
                TodoTask.status != "completed"
            )
        ).count()
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress,
            "overdue": overdue,
            "completion_rate": round(completed / total * 100, 2) if total > 0 else 0,
            "by_priority": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            }
        }
