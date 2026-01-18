# -*- coding: utf-8 -*-
"""
待办任务服务

功能说明：
1. 待办任务管理
2. 每日计划管理
3. 任务提醒

使用示例：
    from app.services.todo_service import TodoService
    
    todo_service = TodoService(db)
    todo = todo_service.create_todo(title="完成文档", description="...")
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
    待办任务服务
    
    功能：
    - 待办任务管理
    - 每日计划管理
    - 任务提醒
    
    使用方法：
        todo_service = TodoService(db)
        todo = todo_service.create_todo(title="完成文档", description="...")
    """
    
    def __init__(self, db: Session):
        """
        初始化待办任务服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.todo_repo = TodoRepository(db)
        self.notification_service = NotificationService(db)
    
    def create_todo(self, title: str, user_id: str, tenant_id: str,
                    description: Optional[str] = None, task_type: str = "personal",
                    priority: str = "medium", due_date: Optional[datetime] = None,
                    due_time: Optional[str] = None, tags: Optional[List[str]] = None,
                    attachment: Optional[str] = None) -> TodoTask:
        """
        创建待办任务
        
        Args:
            title: 任务标题
            user_id: 用户ID
            tenant_id: 租户ID
            description: 任务描述（可选）
            task_type: 任务类型
            priority: 优先级
            due_date: 截止日期（可选）
            due_time: 截止时间（可选）
            tags: 标签列表（可选）
            attachment: 附件URL（可选）
        
        Returns:
            TodoTask: 创建的待办任务对象
        """
        logger.info(f"创建待办任务: title={title}, user_id={user_id}")
        
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
        获取待办任务
        
        Args:
            todo_id: 任务ID
        
        Returns:
            Optional[TodoTask]: 待办任务对象，不存在返回None
        """
        return self.todo_repo.get_todo_by_id(todo_id)
    
    def update_todo(self, todo_id: str, todo_data: Dict[str, Any]) -> Optional[TodoTask]:
        """
        更新待办任务
        
        Args:
            todo_id: 任务ID
            todo_data: 更新数据
        
        Returns:
            Optional[TodoTask]: 更新后的任务对象，不存在返回None
        """
        logger.info(f"更新待办任务: todo_id={todo_id}")
        
        todo = self.todo_repo.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        # 更新任务
        for key, value in todo_data.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        
        return self.todo_repo.update_todo(todo)
    
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
        return self.todo_repo.get_user_todos(user_id, status, priority, page, page_size)
    
    def list_todos(self, user_id: str, status: Optional[str] = None,
                   task_type: Optional[str] = None, priority: Optional[str] = None,
                   is_overdue: Optional[bool] = None, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        获取待办任务列表
        
        Args:
            user_id: 用户ID
            status: 状态（可选）
            task_type: 任务类型（可选）
            priority: 优先级（可选）
            is_overdue: 是否逾期（可选）
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[TodoTask]: 待办任务列表
        """
        if is_overdue is not None:
            return self.todo_repo.get_overdue_todos(page, page_size)
        else:
            return self.todo_repo.get_user_todos(user_id, status, priority, page, page_size)
    
    def complete_todo(self, todo_id: str) -> Optional[TodoTask]:
        """
        完成待办任务
        
        Args:
            todo_id: 任务ID
        
        Returns:
            Optional[TodoTask]: 更新后的任务对象，不存在返回None
        """
        logger.info(f"完成待办任务: todo_id={todo_id}")
        
        todo = self.todo_repo.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        todo.mark_completed()
        return self.todo_repo.update_todo(todo)
    
    def uncomplete_todo(self, todo_id: str) -> Optional[TodoTask]:
        """
        取消完成待办任务
        
        Args:
            todo_id: 任务ID
        
        Returns:
            Optional[TodoTask]: 更新后的任务对象，不存在返回None
        """
        logger.info(f"取消完成待办任务: todo_id={todo_id}")
        
        todo = self.todo_repo.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        todo.mark_pending()
        return self.todo_repo.update_todo(todo)
    
    def delete_todo(self, todo_id: str) -> bool:
        """
        删除待办任务
        
        Args:
            todo_id: 任务ID
        
        Returns:
            bool: 删除是否成功
        """
        logger.info(f"删除待办任务: todo_id={todo_id}")
        return self.todo_repo.delete_todo(todo_id)
    
    def get_overdue_todos(self, page: int = 1, page_size: int = 10) -> List[TodoTask]:
        """
        获取逾期任务
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[TodoTask]: 逾期任务列表
        """
        return self.todo_repo.get_overdue_todos(page, page_size)
    
    def update_overdue_status(self):
        """
        更新所有任务的逾期状态
        """
        logger.info("更新所有任务的逾期状态")
        
        todos = self.todo_repo.get_tenant_todos(tenant_id=None, page=1, page_size=10000)
        for todo in todos:
            todo.update_overdue_status()
            self.todo_repo.update_todo(todo)
    
    def create_daily_plan(self, user_id: str, tenant_id: str, plan_date: date,
                          tasks: List[Dict[str, Any]], notes: Optional[str] = None) -> DailyPlan:
        """
        创建每日计划
        
        Args:
            user_id: 用户ID
            tenant_id: 租户ID
            plan_date: 计划日期
            tasks: 任务列表
            notes: 备注（可选）
        
        Returns:
            DailyPlan: 创建的每日计划对象
        """
        logger.info(f"创建每日计划: user_id={user_id}, plan_date={plan_date}")
        
        daily_plan = DailyPlan(
            tenant_id=tenant_id,
            user_id=user_id,
            plan_date=datetime.combine(plan_date, datetime.min.time()),
            status='active'
        )
        
        return self.todo_repo.create_daily_plan(daily_plan)
    
    def get_user_daily_plan(self, user_id: str, plan_date: date) -> Optional[DailyPlan]:
        """
        获取用户指定日期的每日计划
        
        Args:
            user_id: 用户ID
            plan_date: 计划日期
        
        Returns:
            Optional[DailyPlan]: 每日计划对象，不存在返回None
        """
        return self.todo_repo.get_user_daily_plan(user_id, plan_date)
    
    def get_todo_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户待办任务统计信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        return self.todo_repo.get_todo_statistics(user_id)
    
    def send_overdue_reminders(self):
        """
        发送逾期任务提醒
        """
        logger.info("发送逾期任务提醒")
        
        overdue_todos = self.todo_repo.get_overdue_todos(page=1, page_size=1000)
        for todo in overdue_todos:
            if not todo.reminder_sent:
                # 发送提醒通知
                self.notification_service.send_system_notification(
                    title="任务逾期提醒",
                    content=f"您的任务「{todo.title}」已逾期，请尽快处理！",
                    tenant_id=todo.tenant_id,
                    target_ids=[todo.user_id],
                    priority="high"
                )
                
                # 标记为已发送
                todo.reminder_sent = True
                self.todo_repo.update_todo(todo)
    
    def send_due_date_reminders(self, hours_before: int = 24):
        """
        发送即将到期任务提醒
        
        Args:
            hours_before: 提前小时数
        """
        logger.info(f"发送即将到期任务提醒（提前{hours_before}小时）")
        
        threshold_time = datetime.now() + timedelta(hours=hours_before)
        
        # 获取所有未完成的任务
        all_todos = self.todo_repo.get_tenant_todos(tenant_id=None, page=1, page_size=10000)
        for todo in all_todos:
            if todo.due_date and todo.status != 'completed':
                # 检查是否在提醒时间范围内
                time_diff = (todo.due_date - datetime.now()).total_seconds()
                if 0 < time_diff <= hours_before * 3600:
                    # 发送提醒通知
                    self.notification_service.send_system_notification(
                        title="任务即将到期",
                        content=f"您的任务「{todo.title}」将于{todo.due_date.strftime('%Y-%m-%d %H:%M')}到期，请及时处理！",
                        tenant_id=todo.tenant_id,
                        target_ids=[todo.user_id],
                        priority="medium"
                    )
    
    def count_todos(self, user_id: Optional[str] = None, status: Optional[str] = None) -> int:
        """
        统计待办任务数量
        
        Args:
            user_id: 用户ID（可选）
            status: 状态（可选）
        
        Returns:
            int: 任务数量
        """
        if user_id:
            return self.todo_repo.count_todos_by_user(user_id, status)
        else:
            return self.todo_repo.count_all_todos()