"""
璺ㄦ暟鎹簮浜嬪姟绠＄悊妯″潡锛圫aga妯″紡锛?
鍔熻兘璇存槑锛?1. 鎻愪緵璺ㄦ暟鎹簮鐨勪簨鍔＄鐞?2. 浣跨敤Saga妯″紡瀹炵幇鏈€缁堜竴鑷存€?3. 鏀寔浜嬪姟姝ラ鍜岃ˉ鍋挎搷浣?4. 璁板綍浜嬪姟鎵ц鏃ュ織

浣跨敤绀轰緥锛?    from common.database.transaction import SagaTransaction
    
    # 创建Saga浜嬪姟
    saga = SagaTransaction()
    
    # 娣诲姞姝ラ
    saga.add_step(
        action=create_user,
        compensation=delete_user,
        name='创建鐢ㄦ埛'
    )
    
    saga.add_step(
        action=create_order,
        compensation=cancel_order,
        name='创建璁㈠崟'
    )
    
    # 鎵ц浜嬪姟
    try:
        result = await saga.execute()
        print("浜嬪姟鎵ц鎴愬姛")
    except Exception as e:
        print("浜嬪姟鎵ц澶辫触锛屽凡鍥炴粴")
"""

from typing import Callable, List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger
import json


@dataclass
class SagaStep:
    """
    Saga姝ラ
    
    灞炴€э細
        name: 姝ラ名称
        action: 涓氬姟鎿嶄綔鍑芥暟
        compensation: 琛ュ伩鎿嶄綔鍑芥暟
        result: 鎿嶄綔缁撴灉
        status: 姝ラ状态侊紙pending, success, failed, compensated锛?        error: 閿欒淇℃伅
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
    Saga浜嬪姟绠＄悊鍣?    
    鍔熻兘锛?    - 绠＄悊璺ㄦ暟鎹簮鐨勪簨鍔?    - 鏀寔姝ｅ悜鎵ц鍜岃ˉ鍋垮洖婊?    - 璁板綍浜嬪姟鎵ц鏃ュ織
    - 鏀寔浜嬪姟鎭㈠
    
    浣跨敤鏂规硶锛?        # 创建浜嬪姟
        saga = SagaTransaction(transaction_id='xxx')
        
        # 娣诲姞姝ラ
        saga.add_step(
            action=lambda: create_user(user_data),
            compensation=lambda user_id: delete_user(user_id),
            name='创建鐢ㄦ埛'
        )
        
        # 鎵ц浜嬪姟
        result = await saga.execute()
        
        # 查询浜嬪姟状态?        status = saga.get_status()
    """
    
    def __init__(self, transaction_id: Optional[str] = None):
        """
        鍒濆鍖朣aga浜嬪姟
        
        Args:
            transaction_id: 浜嬪姟ID锛堝彲閫夛紝涓嶄紶鍒欒嚜鍔ㄧ敓鎴愶級
        
        浣跨敤绀轰緥锛?            saga = SagaTransaction()
            # 鎴?            saga = SagaTransaction(transaction_id='custom-id')
        """
        self.transaction_id = transaction_id or self._generate_transaction_id()
        self.steps: List[SagaStep] = []
        self.status = 'pending'
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.error: Optional[str] = None
        
        logger.info(f"创建Saga浜嬪姟: {self.transaction_id}")
    
    def _generate_transaction_id(self) -> str:
        """鐢熸垚浜嬪姟ID"""
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
        娣诲姞浜嬪姟姝ラ
        
        Args:
            action: 涓氬姟鎿嶄綔鍑芥暟锛堟棤鍙傛暟锛岃繑鍥炵粨鏋滐級
            compensation: 琛ュ伩鎿嶄綔鍑芥暟锛堟帴鏀禷ction鐨勭粨鏋滀綔涓哄弬鏁帮級
            name: 姝ラ名称
            **kwargs: 棰濆鐨勬楠ゅ弬鏁?        
        浣跨敤绀轰緥锛?            # 娣诲姞姝ラ
            saga.add_step(
                action=lambda: create_user(username='test'),
                compensation=lambda user_id: delete_user(user_id),
                name='创建鐢ㄦ埛'
            )
            
            # 甯﹀弬鏁扮殑姝ラ
            def create_order(user_id, amount):
                return order_service.create(user_id, amount)
            
            def cancel_order(order_id):
                return order_service.cancel(order_id)
            
            saga.add_step(
                action=lambda: create_order(user_id='xxx', amount=100),
                compensation=lambda order_id: cancel_order(order_id),
                name='创建璁㈠崟'
            )
        """
        step = SagaStep(
            name=name,
            action=action,
            compensation=compensation
        )
        self.steps.append(step)
        logger.debug(f"娣诲姞姝ラ: {name}")
    
    async def execute(self) -> Dict[str, Any]:
        """
        鎵цSaga浜嬪姟
        
        Returns:
            Dict[str, Any]: 浜嬪姟鎵ц缁撴灉
            - success: 鏄惁鎴愬姛
            - transaction_id: 浜嬪姟ID
            - steps: 姝ラ鎵ц缁撴灉
            - error: 閿欒淇℃伅锛堝鏋滃け璐ワ級
        
        Raises:
            Exception: 浜嬪姟鎵ц澶辫触鏃舵姏鍑哄紓甯?        
        浣跨敤绀轰緥锛?            try:
                result = await saga.execute()
                if result['success']:
                    print("浜嬪姟鎵ц鎴愬姛")
                else:
                    print(f"浜嬪姟鎵ц澶辫触: {result['error']}")
            except Exception as e:
                print(f"浜嬪姟鎵ц寮傚父: {e}")
        """
        logger.info(f"寮€濮嬫墽琛孲aga浜嬪姟: {self.transaction_id}")
        logger.info(f"鎬绘楠ゆ暟: {len(self.steps)}")
        
        self.status = 'running'
        executed_steps: List[SagaStep] = []
        
        try:
            # 姝ｅ悜鎵ц鎵€鏈夋楠?            for i, step in enumerate(self.steps):
                logger.info(f"鎵ц姝ラ {i + 1}/{len(self.steps)}: {step.name}")
                
                try:
                    # 鎵ц涓氬姟鎿嶄綔
                    step.result = await step.action()
                    step.status = 'success'
                    executed_steps.append(step)
                    logger.success(f"姝ラ {step.name} 鎵ц鎴愬姛")
                    
                except Exception as e:
                    step.status = 'failed'
                    step.error = str(e)
                    logger.error(f"姝ラ {step.name} 鎵ц澶辫触: {e}")
                    
                    # 鎵ц琛ュ伩鎿嶄綔
                    await self._compensate(executed_steps)
                    
                    self.status = 'failed'
                    self.error = str(e)
                    self.completed_at = datetime.now()
                    
                    raise Exception(f"浜嬪姟鎵ц澶辫触: {e}")
            
            # 鎵€鏈夋楠ゆ墽琛屾垚鍔?            self.status = 'completed'
            self.completed_at = datetime.now()
            
            logger.success(f"Saga浜嬪姟 {self.transaction_id} 鎵ц鎴愬姛")
            
            return {
                'success': True,
                'transaction_id': self.transaction_id,
                'steps': [self._step_to_dict(step) for step in self.steps],
                'status': self.status
            }
            
        except Exception as e:
            logger.error(f"Saga浜嬪姟 {self.transaction_id} 鎵ц澶辫触: {e}")
            raise
    
    async def _compensate(self, executed_steps: List[SagaStep]):
        """
        鎵ц琛ュ伩鎿嶄綔
        
        Args:
            executed_steps: 宸叉墽琛岀殑姝ラ鍒楄〃
        
        浣跨敤绀轰緥锛?            # 鍐呴儴鏂规硶锛岃嚜鍔ㄨ皟鐢?            await saga._compensate(executed_steps)
        """
        logger.warning(f"寮€濮嬫墽琛岃ˉ鍋挎搷浣滐紝鍏?{len(executed_steps)} 涓楠?)
        
        # 鍙嶅悜鎵ц琛ュ伩鎿嶄綔
        for i in range(len(executed_steps) - 1, -1, -1):
            step = executed_steps[i]
            
            if step.status != 'success':
                continue
            
            logger.info(f"鎵ц琛ュ伩姝ラ: {step.name}")
            
            try:
                # 鎵ц琛ュ伩鎿嶄綔
                await step.compensation(step.result)
                step.status = 'compensated'
                logger.success(f"琛ュ伩姝ラ {step.name} 鎵ц鎴愬姛")
                
            except Exception as e:
                step.error = str(e)
                logger.error(f"琛ュ伩姝ラ {step.name} 鎵ц澶辫触: {e}")
                # 琛ュ伩澶辫触锛岃褰曚絾缁х画鎵ц鍏朵粬琛ュ伩
    
    def get_status(self) -> Dict[str, Any]:
        """
        鑾峰彇浜嬪姟状态?        
        Returns:
            Dict[str, Any]: 浜嬪姟状态佷俊鎭?            - transaction_id: 浜嬪姟ID
            - status: 浜嬪姟状态?            - steps: 姝ラ状态?            - created_at: 创建时间
            - completed_at: 瀹屾垚鏃堕棿
            - error: 閿欒淇℃伅
        
        浣跨敤绀轰緥锛?            status = saga.get_status()
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
        灏嗘楠よ浆鎹负瀛楀吀
        
        Args:
            step: Saga姝ラ瀵硅薄
        
        Returns:
            Dict[str, Any]: 姝ラ瀛楀吀
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
    Saga缂栨帓鍣紙楂樼骇鐢ㄦ硶锛?    
    鍔熻兘锛?    - 绠＄悊澶氫釜Saga浜嬪姟
    - 鏀寔浜嬪姟缂栨帓
    - 鎻愪緵浜嬪姟鐩戞帶
    
    浣跨敤鏂规硶锛?        orchestrator = SagaOrchestrator()
        
        # 创建骞舵墽琛屼簨鍔?        saga = orchestrator.create_transaction()
        saga.add_step(...)
        result = await orchestrator.execute(saga)
        
        # 查询鎵€鏈変簨鍔?        transactions = orchestrator.list_transactions()
    """
    
    def __init__(self):
        """鍒濆鍖朣aga缂栨帓鍣?""
        self.transactions: Dict[str, SagaTransaction] = {}
        logger.info("Saga缂栨帓鍣ㄥ垵濮嬪寲瀹屾垚")
    
    def create_transaction(self, transaction_id: Optional[str] = None) -> SagaTransaction:
        """
        创建鏂扮殑Saga浜嬪姟
        
        Args:
            transaction_id: 浜嬪姟ID锛堝彲閫夛級
        
        Returns:
            SagaTransaction: Saga浜嬪姟瀵硅薄
        
        浣跨敤绀轰緥锛?            orchestrator = SagaOrchestrator()
            saga = orchestrator.create_transaction()
        """
        saga = SagaTransaction(transaction_id)
        self.transactions[saga.transaction_id] = saga
        return saga
    
    async def execute(self, saga: SagaTransaction) -> Dict[str, Any]:
        """
        鎵цSaga浜嬪姟
        
        Args:
            saga: Saga浜嬪姟瀵硅薄
        
        Returns:
            Dict[str, Any]: 鎵ц缁撴灉
        
        浣跨敤绀轰緥锛?            orchestrator = SagaOrchestrator()
            saga = orchestrator.create_transaction()
            saga.add_step(...)
            result = await orchestrator.execute(saga)
        """
        return await saga.execute()
    
    def get_transaction(self, transaction_id: str) -> Optional[SagaTransaction]:
        """
        鑾峰彇鎸囧畾鐨勪簨鍔?        
        Args:
            transaction_id: 浜嬪姟ID
        
        Returns:
            Optional[SagaTransaction]: Saga浜嬪姟瀵硅薄锛堝鏋滃瓨鍦級
        
        浣跨敤绀轰緥锛?            saga = orchestrator.get_transaction('saga-xxx')
        """
        return self.transactions.get(transaction_id)
    
    def list_transactions(self, status: Optional[str] = None) -> List[SagaTransaction]:
        """
        鍒楀嚭鎵€鏈変簨鍔?        
        Args:
            status: 状态佽繃婊わ紙鍙€夛級
        
        Returns:
            List[SagaTransaction]: 浜嬪姟鍒楄〃
        
        浣跨敤绀轰緥锛?            # 鍒楀嚭鎵€鏈変簨鍔?            all_transactions = orchestrator.list_transactions()
            
            # 鍒楀嚭澶辫触鐨勪簨鍔?            failed_transactions = orchestrator.list_transactions(status='failed')
        """
        if status:
            return [t for t in self.transactions.values() if t.status == status]
        return list(self.transactions.values())
    
    def cleanup(self, older_than_hours: int = 24):
        """
        娓呯悊鏃х殑浜嬪姟璁板綍
        
        Args:
            older_than_hours: 娓呯悊澶氬皯灏忔椂鍓嶇殑浜嬪姟
        
        浣跨敤绀轰緥锛?            orchestrator.cleanup(older_than_hours=24)
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        to_remove = []
        
        for transaction_id, saga in self.transactions.items():
            if saga.completed_at and saga.completed_at < cutoff_time:
                to_remove.append(transaction_id)
        
        for transaction_id in to_remove:
            del self.transactions[transaction_id]
            logger.info(f"娓呯悊浜嬪姟: {transaction_id}")
        
        logger.info(f"娓呯悊瀹屾垚锛屽叡娓呯悊 {len(to_remove)} 涓簨鍔?)


# 鍏ㄥ眬瀹炰緥
saga_orchestrator = SagaOrchestrator()
