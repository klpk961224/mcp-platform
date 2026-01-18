"""
閿欒鐮丷epository

鎻愪緵閿欒鐮佹暟鎹闂眰
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from common.database.models.system import ErrorCode


class ErrorCodeRepository:
    """閿欒鐮丷epository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, error_code_id: str) -> Optional[ErrorCode]:
        """鏍规嵁ID鑾峰彇閿欒鐮?""
        return self.db.query(ErrorCode).filter(ErrorCode.id == error_code_id).first()

    def get_by_code(self, code: str) -> Optional[ErrorCode]:
        """鏍规嵁閿欒鐮佽幏鍙?""
        return self.db.query(ErrorCode).filter(ErrorCode.code == code).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ErrorCode]:
        """鑾峰彇鎵€鏈夐敊璇爜"""
        return self.db.query(ErrorCode).offset(skip).limit(limit).all()

    def get_by_module(self, module: str, skip: int = 0, limit: int = 100) -> List[ErrorCode]:
        """鏍规嵁妯″潡鑾峰彇閿欒鐮?""
        return self.db.query(ErrorCode).filter(ErrorCode.module == module).offset(skip).limit(limit).all()

    def get_by_level(self, level: str, skip: int = 0, limit: int = 100) -> List[ErrorCode]:
        """鏍规嵁閿欒绾у埆鑾峰彇閿欒鐮?""
        return self.db.query(ErrorCode).filter(ErrorCode.level == level).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """鎼滅储閿欒鐮?""
        query = self.db.query(ErrorCode)

        # 閿欒鐮佹悳绱?        if query_params.get("code"):
            query = query.filter(ErrorCode.code.like(f"%{query_params['code']}%"))

        # 閿欒淇℃伅鎼滅储
        if query_params.get("message"):
            query = query.filter(ErrorCode.message.like(f"%{query_params['message']}%"))

        # 妯″潡杩囨护
        if query_params.get("module"):
            query = query.filter(ErrorCode.module == query_params["module"])

        # 閿欒绾у埆杩囨护
        if query_params.get("level"):
            query = query.filter(ErrorCode.level == query_params["level"])

        # 鐘舵€佽繃婊?        if query_params.get("status"):
            query = query.filter(ErrorCode.status == query_params["status"])

        # 缁熻鎬绘暟
        total = query.count()

        # 鍒嗛〉
        error_codes = query.offset(skip).limit(limit).all()

        return error_codes, total

    def create(self, error_code: ErrorCode) -> ErrorCode:
        """鍒涘缓閿欒鐮?""
        self.db.add(error_code)
        self.db.commit()
        self.db.refresh(error_code)
        return error_code

    def update(self, error_code: ErrorCode) -> ErrorCode:
        """鏇存柊閿欒鐮?""
        self.db.commit()
        self.db.refresh(error_code)
        return error_code

    def delete(self, error_code_id: str) -> bool:
        """鍒犻櫎閿欒鐮?""
        error_code = self.get_by_id(error_code_id)
        if error_code:
            self.db.delete(error_code)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """缁熻閿欒鐮佹暟閲?""
        return self.db.query(ErrorCode).count()

    def count_by_module(self, module: str) -> int:
        """鏍规嵁妯″潡缁熻閿欒鐮佹暟閲?""
        return self.db.query(ErrorCode).filter(ErrorCode.module == module).count()

    def count_by_level(self, level: str) -> int:
        """鏍规嵁閿欒绾у埆缁熻閿欒鐮佹暟閲?""
        return self.db.query(ErrorCode).filter(ErrorCode.level == level).count()
