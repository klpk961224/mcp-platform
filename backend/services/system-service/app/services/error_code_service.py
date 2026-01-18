"""
閿欒鐮丼ervice

鎻愪緵閿欒鐮佷笟鍔￠€昏緫灞?"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from common.database.models.system import ErrorCode
from app.repositories.error_code_repository import ErrorCodeRepository


class ErrorCodeService:
    """閿欒鐮丼ervice"""

    # 閿欒绾у埆甯搁噺
    LEVEL_INFO = "info"
    LEVEL_WARNING = "warning"
    LEVEL_ERROR = "error"
    LEVEL_CRITICAL = "critical"

    # 鐘舵€佸父閲?    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    def __init__(self, db: Session):
        self.db = db
        self.repository = ErrorCodeRepository(db)

    def get_error_code_by_id(self, error_code_id: str) -> Optional[Dict[str, Any]]:
        """鏍规嵁ID鑾峰彇閿欒鐮?""
        error_code = self.repository.get_by_id(error_code_id)
        if not error_code:
            return None
        return self._to_dict(error_code)

    def get_error_code_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """鏍规嵁閿欒鐮佽幏鍙?""
        error_code = self.repository.get_by_code(code)
        if not error_code:
            return None
        return self._to_dict(error_code)

    def get_all_error_codes(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鑾峰彇鎵€鏈夐敊璇爜"""
        error_codes = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {
            "items": [self._to_dict(ec) for ec in error_codes],
            "total": total
        }

    def get_error_codes_by_module(self, module: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鏍规嵁妯″潡鑾峰彇閿欒鐮?""
        error_codes = self.repository.get_by_module(module, skip=skip, limit=limit)
        total = self.repository.count_by_module(module)
        return {
            "items": [self._to_dict(ec) for ec in error_codes],
            "total": total
        }

    def get_error_codes_by_level(self, level: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """鏍规嵁閿欒绾у埆鑾峰彇閿欒鐮?""
        error_codes = self.repository.get_by_level(level, skip=skip, limit=limit)
        total = self.repository.count_by_level(level)
        return {
            "items": [self._to_dict(ec) for ec in error_codes],
            "total": total
        }

    def search_error_codes(
        self,
        query_params: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """鎼滅储閿欒鐮?""
        error_codes, total = self.repository.search(query_params, skip=skip, limit=limit)
        return {
            "items": [self._to_dict(ec) for ec in error_codes],
            "total": total
        }

    def create_error_code(
        self,
        code: str,
        message: str,
        module: str,
        level: str = LEVEL_ERROR,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """鍒涘缓閿欒鐮?""
        # 妫€鏌ラ敊璇爜鏄惁宸插瓨鍦?        existing = self.repository.get_by_code(code)
        if existing:
            raise ValueError(f"閿欒鐮?{code} 宸插瓨鍦?)

        # 鍒涘缓閿欒鐮?        error_code = ErrorCode(
            code=code,
            message=message,
            level=level,
            module=module,
            description=description,
            status=self.STATUS_ACTIVE
        )

        error_code = self.repository.create(error_code)
        return self._to_dict(error_code)

    def update_error_code(
        self,
        error_code_id: str,
        code: Optional[str] = None,
        message: Optional[str] = None,
        level: Optional[str] = None,
        module: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """鏇存柊閿欒鐮?""
        error_code = self.repository.get_by_id(error_code_id)
        if not error_code:
            return None

        # 鏇存柊瀛楁
        if code is not None:
            error_code.code = code
        if message is not None:
            error_code.message = message
        if level is not None:
            error_code.level = level
        if module is not None:
            error_code.module = module
        if description is not None:
            error_code.description = description
        if status is not None:
            error_code.status = status

        error_code = self.repository.update(error_code)
        return self._to_dict(error_code)

    def delete_error_code(self, error_code_id: str) -> bool:
        """鍒犻櫎閿欒鐮?""
        return self.repository.delete(error_code_id)

    def get_statistics(self) -> Dict[str, Any]:
        """鑾峰彇閿欒鐮佺粺璁′俊鎭?""
        total = self.repository.count()

        # 鎸夌骇鍒粺璁?        level_stats = {}
        for level in [self.LEVEL_INFO, self.LEVEL_WARNING, self.LEVEL_ERROR, self.LEVEL_CRITICAL]:
            level_stats[level] = self.repository.count_by_level(level)

        # 鎸夌姸鎬佺粺璁?        active_count = self.repository.search({"status": self.STATUS_ACTIVE}, skip=0, limit=999999)[1]
        inactive_count = self.repository.search({"status": self.STATUS_INACTIVE}, skip=0, limit=999999)[1]

        return {
            "total": total,
            "by_level": level_stats,
            "by_status": {
                "active": active_count,
                "inactive": inactive_count
            }
        }

    def _to_dict(self, error_code: ErrorCode) -> Dict[str, Any]:
        """杞崲涓哄瓧鍏?""
        return {
            "id": error_code.id,
            "code": error_code.code,
            "message": error_code.message,
            "level": error_code.level,
            "module": error_code.module,
            "description": error_code.description,
            "status": error_code.status,
            "created_at": error_code.created_at.isoformat() if error_code.created_at else None,
            "updated_at": error_code.updated_at.isoformat() if error_code.updated_at else None
        }
