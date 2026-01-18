"""
跨数据源事务管理模块（Saga模式）

功能说明：
1. 提供跨数据源的事务管理
2. 使用Saga模式实现最终一致性
3. 支持事务步骤和补偿操作
4. 记录事务执行日志

使用示例：
    from common.database.transaction import SagaTransaction
    
    # 创建Saga事务
    saga = SagaTransaction()
    
    # 添加步骤
    saga.add_step(
        action=create_user,
        compensation=delete_user,
        name='创建用户'
    )
    
    saga.add_step(
        action=create_order,
        compensation=cancel_order,
        name='创建订单'
    )
    
    # 执行事务
    try:
        result = await saga.execute()
        print("事务执行成功")
    except Exception as e:
        print("事务执行失败，已回滚")
"""

from typing import Callable, List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger
import json


@dataclass
class SagaStep:
    """
    Saga步骤
    
    属性：
        name: 步骤名称
        action: 业务操作函数
        compensation: 补偿操作函数
        result: 操作结果
        status: 步骤状态（pending, success, failed, compensated）
        error: 错误信息
    """
    name: str
    action: Callable
    compensation: Callable
    result: Any = None
    status: str = 'pending'
    error: Optional[str] = None
    
    def __repr__(self):
        return f"<SagaStep(name='{self.name}', status='{self.status}')>"


class SagaTransaction:
    """
    Saga事务管理器
    
    功能：
    - 管理跨数据源的事务
    - 支持正向执行和补偿回滚
    - 记录事务执行日志
    - 支持事务恢复
    
    使用方法：
        # 创建事务
        saga = SagaTransaction(transaction_id='xxx')
        
        # 添加步骤
        saga.add_step(
            action=lambda: create_user(user_data),
            compensation=lambda user_id: delete_user(user_id),
            name='创建用户'
        )
        
        # 执行事务
        result = await saga.execute()
        
        # 查询事务状态
        status = saga.get_status()
    """
    
    def __init__(self, transaction_id: Optional[str] = None):
        """
        初始化Saga事务
        
        Args:
            transaction_id: 事务ID（可选，不传则自动生成）
        
        使用示例：
            saga = SagaTransaction()
            # 或
            saga = SagaTransaction(transaction_id='custom-id')
        """
        self.transaction_id = transaction_id or self._generate_transaction_id()
        self.steps: List[SagaStep] = []
        self.status = 'pending'
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.error: Optional[str] = None
        
        logger.info(f"创建Saga事务: {self.transaction_id}")
    
    def _generate_transaction_id(self) -> str:
        """生成事务ID"""
        import uuid
        return f"saga-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    
    def add_step(
        self,
        action: Callable,
        compensation: Callable,
        name: str,
        **kwargs
    ):
        """
        添加事务步骤
        
        Args:
            action: 业务操作函数（无参数，返回结果）
            compensation: 补偿操作函数（接收action的结果作为参数）
            name: 步骤名称
            **kwargs: 额外的步骤参数
        
        使用示例：
            # 添加步骤
            saga.add_step(
                action=lambda: create_user(username='test'),
                compensation=lambda user_id: delete_user(user_id),
                name='创建用户'
            )
            
            # 带参数的步骤
            def create_order(user_id, amount):
                return order_service.create(user_id, amount)
            
            def cancel_order(order_id):
                return order_service.cancel(order_id)
            
            saga.add_step(
                action=lambda: create_order(user_id='xxx', amount=100),
                compensation=lambda order_id: cancel_order(order_id),
                name='创建订单'
            )
        """
        step = SagaStep(
            name=name,
            action=action,
            compensation=compensation
        )
        self.steps.append(step)
        logger.debug(f"添加步骤: {name}")
    
    async def execute(self) -> Dict[str, Any]:
        """
        执行Saga事务
        
        Returns:
            Dict[str, Any]: 事务执行结果
            - success: 是否成功
            - transaction_id: 事务ID
            - steps: 步骤执行结果
            - error: 错误信息（如果失败）
        
        Raises:
            Exception: 事务执行失败时抛出异常
        
        使用示例：
            try:
                result = await saga.execute()
                if result['success']:
                    print("事务执行成功")
                else:
                    print(f"事务执行失败: {result['error']}")
            except Exception as e:
                print(f"事务执行异常: {e}")
        """
        logger.info(f"开始执行Saga事务: {self.transaction_id}")
        logger.info(f"总步骤数: {len(self.steps)}")
        
        self.status = 'running'
        executed_steps: List[SagaStep] = []
        
        try:
            # 正向执行所有步骤
            for i, step in enumerate(self.steps):
                logger.info(f"执行步骤 {i + 1}/{len(self.steps)}: {step.name}")
                
                try:
                    # 执行业务操作
                    step.result = await step.action()
                    step.status = 'success'
                    executed_steps.append(step)
                    logger.success(f"步骤 {step.name} 执行成功")
                    
                except Exception as e:
                    step.status = 'failed'
                    step.error = str(e)
                    logger.error(f"步骤 {step.name} 执行失败: {e}")
                    
                    # 执行补偿操作
                    await self._compensate(executed_steps)
                    
                    self.status = 'failed'
                    self.error = str(e)
                    self.completed_at = datetime.now()
                    
                    raise Exception(f"事务执行失败: {e}")
            
            # 所有步骤执行成功
            self.status = 'completed'
            self.completed_at = datetime.now()
            
            logger.success(f"Saga事务 {self.transaction_id} 执行成功")
            
            return {
                'success': True,
                'transaction_id': self.transaction_id,
                'steps': [self._step_to_dict(step) for step in self.steps],
                'status': self.status
            }
            
        except Exception as e:
            logger.error(f"Saga事务 {self.transaction_id} 执行失败: {e}")
            raise
    
    async def _compensate(self, executed_steps: List[SagaStep]):
        """
        执行补偿操作
        
        Args:
            executed_steps: 已执行的步骤列表
        
        使用示例：
            # 内部方法，自动调用
            await saga._compensate(executed_steps)
        """
        logger.warning(f"开始执行补偿操作，共 {len(executed_steps)} 个步骤")
        
        # 反向执行补偿操作
        for i in range(len(executed_steps) - 1, -1, -1):
            step = executed_steps[i]
            
            if step.status != 'success':
                continue
            
            logger.info(f"执行补偿步骤: {step.name}")
            
            try:
                # 执行补偿操作
                await step.compensation(step.result)
                step.status = 'compensated'
                logger.success(f"补偿步骤 {step.name} 执行成功")
                
            except Exception as e:
                step.error = str(e)
                logger.error(f"补偿步骤 {step.name} 执行失败: {e}")
                # 补偿失败，记录但继续执行其他补偿
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取事务状态
        
        Returns:
            Dict[str, Any]: 事务状态信息
            - transaction_id: 事务ID
            - status: 事务状态
            - steps: 步骤状态
            - created_at: 创建时间
            - completed_at: 完成时间
            - error: 错误信息
        
        使用示例：
            status = saga.get_status()
            print(status)
            # {
            #     'transaction_id': 'saga-xxx',
            #     'status': 'completed',
            #     'steps': [...],
            #     'created_at': '2024-01-15 10:00:00',
            #     'completed_at': '2024-01-15 10:00:05',
            #     'error': None
            # }
        """
        return {
            'transaction_id': self.transaction_id,
            'status': self.status,
            'steps': [self._step_to_dict(step) for step in self.steps],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error': self.error
        }
    
    def _step_to_dict(self, step: SagaStep) -> Dict[str, Any]:
        """
        将步骤转换为字典
        
        Args:
            step: Saga步骤对象
        
        Returns:
            Dict[str, Any]: 步骤字典
        """
        return {
            'name': step.name,
            'status': step.status,
            'error': step.error
        }
    
    def __repr__(self):
        return f"<SagaTransaction(id='{self.transaction_id}', status='{self.status}')>"


class SagaOrchestrator:
    """
    Saga编排器（高级用法）
    
    功能：
    - 管理多个Saga事务
    - 支持事务编排
    - 提供事务监控
    
    使用方法：
        orchestrator = SagaOrchestrator()
        
        # 创建并执行事务
        saga = orchestrator.create_transaction()
        saga.add_step(...)
        result = await orchestrator.execute(saga)
        
        # 查询所有事务
        transactions = orchestrator.list_transactions()
    """
    
    def __init__(self):
        """初始化Saga编排器"""
        self.transactions: Dict[str, SagaTransaction] = {}
        logger.info("Saga编排器初始化完成")
    
    def create_transaction(self, transaction_id: Optional[str] = None) -> SagaTransaction:
        """
        创建新的Saga事务
        
        Args:
            transaction_id: 事务ID（可选）
        
        Returns:
            SagaTransaction: Saga事务对象
        
        使用示例：
            orchestrator = SagaOrchestrator()
            saga = orchestrator.create_transaction()
        """
        saga = SagaTransaction(transaction_id)
        self.transactions[saga.transaction_id] = saga
        return saga
    
    async def execute(self, saga: SagaTransaction) -> Dict[str, Any]:
        """
        执行Saga事务
        
        Args:
            saga: Saga事务对象
        
        Returns:
            Dict[str, Any]: 执行结果
        
        使用示例：
            orchestrator = SagaOrchestrator()
            saga = orchestrator.create_transaction()
            saga.add_step(...)
            result = await orchestrator.execute(saga)
        """
        return await saga.execute()
    
    def get_transaction(self, transaction_id: str) -> Optional[SagaTransaction]:
        """
        获取指定的事务
        
        Args:
            transaction_id: 事务ID
        
        Returns:
            Optional[SagaTransaction]: Saga事务对象（如果存在）
        
        使用示例：
            saga = orchestrator.get_transaction('saga-xxx')
        """
        return self.transactions.get(transaction_id)
    
    def list_transactions(self, status: Optional[str] = None) -> List[SagaTransaction]:
        """
        列出所有事务
        
        Args:
            status: 状态过滤（可选）
        
        Returns:
            List[SagaTransaction]: 事务列表
        
        使用示例：
            # 列出所有事务
            all_transactions = orchestrator.list_transactions()
            
            # 列出失败的事务
            failed_transactions = orchestrator.list_transactions(status='failed')
        """
        if status:
            return [t for t in self.transactions.values() if t.status == status]
        return list(self.transactions.values())
    
    def cleanup(self, older_than_hours: int = 24):
        """
        清理旧的事务记录
        
        Args:
            older_than_hours: 清理多少小时前的事务
        
        使用示例：
            orchestrator.cleanup(older_than_hours=24)
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        to_remove = []
        
        for transaction_id, saga in self.transactions.items():
            if saga.completed_at and saga.completed_at < cutoff_time:
                to_remove.append(transaction_id)
        
        for transaction_id in to_remove:
            del self.transactions[transaction_id]
            logger.info(f"清理事务: {transaction_id}")
        
        logger.info(f"清理完成，共清理 {len(to_remove)} 个事务")


# 全局实例
saga_orchestrator = SagaOrchestrator()