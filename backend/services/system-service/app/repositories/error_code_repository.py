"""
错误码Repository

提供错误码数据访问层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from common.database.models.system import ErrorCode


class ErrorCodeRepository:
    """错误码Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, error_code_id: str) -> Optional[ErrorCode]:
        """根据ID获取错误码"""
        return self.db.query(ErrorCode).filter(ErrorCode.id == error_code_id).first()

    def get_by_code(self, code: str) -> Optional[ErrorCode]:
        """根据错误码获取"""
        return self.db.query(ErrorCode).filter(ErrorCode.code == code).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ErrorCode]:
        """获取所有错误码"""
        return self.db.query(ErrorCode).offset(skip).limit(limit).all()

    def get_by_module(self, module: str, skip: int = 0, limit: int = 100) -> List[ErrorCode]:
        """根据模块获取错误码"""
        return self.db.query(ErrorCode).filter(ErrorCode.module == module).offset(skip).limit(limit).all()

    def get_by_level(self, level: str, skip: int = 0, limit: int = 100) -> List[ErrorCode]:
        """根据错误级别获取错误码"""
        return self.db.query(ErrorCode).filter(ErrorCode.level == level).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """搜索错误码"""
        query = self.db.query(ErrorCode)

        # 错误码搜索
        if query_params.get("code"):
            query = query.filter(ErrorCode.code.like(f"%{query_params['code']}%"))

        # 错误信息搜索
        if query_params.get("message"):
            query = query.filter(ErrorCode.message.like(f"%{query_params['message']}%"))

        # 模块过滤
        if query_params.get("module"):
            query = query.filter(ErrorCode.module == query_params["module"])

        # 错误级别过滤
        if query_params.get("level"):
            query = query.filter(ErrorCode.level == query_params["level"])

        # 状态过滤
        if query_params.get("status"):
            query = query.filter(ErrorCode.status == query_params["status"])

        # 统计总数
        total = query.count()

        # 分页
        error_codes = query.offset(skip).limit(limit).all()

        return error_codes, total

    def create(self, error_code: ErrorCode) -> ErrorCode:
        """创建错误码"""
        self.db.add(error_code)
        self.db.commit()
        self.db.refresh(error_code)
        return error_code

    def update(self, error_code: ErrorCode) -> ErrorCode:
        """更新错误码"""
        self.db.commit()
        self.db.refresh(error_code)
        return error_code

    def delete(self, error_code_id: str) -> bool:
        """删除错误码"""
        error_code = self.get_by_id(error_code_id)
        if error_code:
            self.db.delete(error_code)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """统计错误码数量"""
        return self.db.query(ErrorCode).count()

    def count_by_module(self, module: str) -> int:
        """根据模块统计错误码数量"""
        return self.db.query(ErrorCode).filter(ErrorCode.module == module).count()

    def count_by_level(self, level: str) -> int:
        """根据错误级别统计错误码数量"""
        return self.db.query(ErrorCode).filter(ErrorCode.level == level).count()