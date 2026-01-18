# -*- coding: utf-8 -*-
"""
待办任务模型

功能说明：
1. 个人待办任务管理
2. 每日计划管理
3. 任务提醒

使用示例：
    from app.models.todo import TodoTask, DailyPlan
    
    # 创建待办任务
    todo = TodoTask(
        title="完成项目文档",
        description="编写项目设计文档",
        priority="high"
    )
"""

from common.database.models.todo import TodoTask, DailyPlan

# 重新导出模型，方便使用
__all__ = ['TodoTask', 'DailyPlan']