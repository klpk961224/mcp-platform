# -*- coding: utf-8 -*-
"""
待办任务数据访问层

功能说明：
1. 待办任务CRUD操作
2. 每日计划CRUD操作
3. 待办任务查询和统计

使用示例：
    from app.repositories.todo_repository import TodoRepository
    
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
    待办任务数据访问层
    
    功能：
    - 待办任务CRUD操作
    - 每日计划CRUD操作
    - 待办任务查询和统计
    
    使用方法：
        todo_repo = TodoRepository(db)
        todos = todo_repo.get_user_todos(user_id="123")
    """
    
    def __init__(self, db: Session):
        """
        初始化待办任务数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    # 待办任务相关方法
    def create_todo(self, todo: TodoTask) -> TodoTask:
        """
        创建待办任务
        
        Args:
            todo: 待办任务对象
        
        Returns:
            TodoTask: 创建的待办任务对象
        """
        logger.info(f"创建待办任务: title={todo.title}, user_id={todo.user_id}")
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def get_todo_by_id(self, todo_id: str) -> Optional[TodoTask]:
        """
        根据ID获取待办任务
        
        Args:
            todo_id: 任务ID
        
        Returns:
            Optional[TodoTask]: 待办任务对象，不存在返回None
        """
        return self.db.query(TodoTask).filter(TodoTask.id == todo_id).first()
    
    def get_user_todos(self, user_id: str, status: Optional[str] = None,
                       priority: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        获取用户待办任务
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
            priority: 优先级（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[TodoTask]: 待办任务列表
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
        获取租户待办任务
        
        Args:
            tenant_id: 租户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[TodoTask]: 待办任务列表
        """
        offset = (page - 1) * page_size
        return self.db.query(TodoTask).filter(
            TodoTask.tenant_id == tenant_id
        ).order_by(TodoTask.created_at.desc()).offset(offset).limit(page_size).all()
    
    def get_overdue_todos(self, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        获取逾期任务
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[TodoTask]: 逾期任务列表
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
        搜索待办任务
        
        Args:
            keyword: 关键词
            tenant_id: 租户ID（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[TodoTask]: 待办任务列表
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
        更新待办任务
        
        Args:
            todo: 待办任务对象
        
        Returns:
            TodoTask: 更新后的待办任务对象
        """
        logger.info(f"更新待办任务: todo_id={todo.id}")
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def delete_todo(self, todo_id: str) -> bool:
        """
        删除待办任务
        
        Args:
            todo_id: 任务ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除待办任务: todo_id={todo_id}")
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        self.db.delete(todo)
        self.db.commit()
        return True
    
    # 每日计划相关方法
    def create_daily_plan(self, daily_plan: DailyPlan) -> DailyPlan:
        """
        创建每日计划
        
        Args:
            daily_plan: 每日计划对象
        
        Returns:
            DailyPlan: 创建的每日计划对象
        """
        logger.info(f"创建每日计划: user_id={daily_plan.user_id}, plan_date={daily_plan.plan_date}")
        self.db.add(daily_plan)
        self.db.commit()
        self.db.refresh(daily_plan)
        return daily_plan
    
    def get_daily_plan_by_id(self, plan_id: str) -> Optional[DailyPlan]:
        """
        根据ID获取每日计划
        
        Args:
            plan_id: 计划ID
        
        Returns:
            Optional[DailyPlan]: 每日计划对象，不存在返回None
        """
        return self.db.query(DailyPlan).filter(DailyPlan.id == plan_id).first()
    
    def get_user_daily_plan(self, user_id: str, plan_date: date) -> Optional[DailyPlan]:
        """
        获取用户指定日期的每日计划
        
        Args:
            user_id: 用户ID
            plan_date: 计划日期
        
        Returns:
            Optional[DailyPlan]: 每日计划对象，不存在返回None
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
        获取用户每日计划列表
        
        Args:
            user_id: 用户ID
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[DailyPlan]: 每日计划列表
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
        更新每日计划
        
        Args:
            daily_plan: 每日计划对象
        
        Returns:
            DailyPlan: 更新后的每日计划对象
        """
        logger.info(f"更新每日计划: plan_id={daily_plan.id}")
        self.db.commit()
        self.db.refresh(daily_plan)
        return daily_plan
    
    def delete_daily_plan(self, plan_id: str) -> bool:
        """
        删除每日计划
        
        Args:
            plan_id: 计划ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除每日计划: plan_id={plan_id}")
        daily_plan = self.get_daily_plan_by_id(plan_id)
        if not daily_plan:
            return False
        
        self.db.delete(daily_plan)
        self.db.commit()
        return True
    
    # 统计方法
    def count_todos_by_user(self, user_id: str, status: Optional[str] = None) -> int:
        """
        统计用户待办任务数量
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
        
        Returns:
            int: 任务数量
        """
        query = self.db.query(TodoTask).filter(TodoTask.user_id == user_id)
        if status:
            query = query.filter(TodoTask.status == status)
        return query.count()
    
    def count_overdue_todos(self, user_id: str) -> int:
        """
        统计用户逾期任务数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 逾期任务数量
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
        统计所有待办任务数量
        
        Returns:
            int: 任务数量
        """
        return self.db.query(TodoTask).count()
    
    def get_todo_statistics(self, user_id: str) -> dict:
        """
        获取用户待办任务统计信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            dict: 统计信息
        """
        total = self.count_todos_by_user(user_id)
        completed = self.count_todos_by_user(user_id, "completed")
        pending = self.count_todos_by_user(user_id, "pending")
        in_progress = self.count_todos_by_user(user_id, "in_progress")
        overdue = self.count_overdue_todos(user_id)
        
        # 按优先级统计
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