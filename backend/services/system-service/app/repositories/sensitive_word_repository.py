"""
鏁忔劅璇峈epository

鎻愪緵鏁忔劅璇嶆暟鎹闂眰
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from common.database.models.sensitive_word import SensitiveWord


class SensitiveWordRepository:
    """鏁忔劅璇峈epository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sensitive_word_id: str) -> Optional[SensitiveWord]:
        """鏍规嵁ID鑾峰彇鏁忔劅璇?""
        return self.db.query(SensitiveWord).filter(SensitiveWord.id == sensitive_word_id).first()

    def get_by_word(self, word: str) -> Optional[SensitiveWord]:
        """鏍规嵁鏁忔劅璇嶈幏鍙?""
        return self.db.query(SensitiveWord).filter(SensitiveWord.word == word).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SensitiveWord]:
        """鑾峰彇鎵€鏈夋晱鎰熻瘝"""
        return self.db.query(SensitiveWord).order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[SensitiveWord]:
        """鏍规嵁鍒嗙被鑾峰彇鏁忔劅璇?""
        return self.db.query(SensitiveWord).filter(
            SensitiveWord.category == category,
            SensitiveWord.status == "active"
        ).order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

    def get_by_level(self, level: int, skip: int = 0, limit: int = 100) -> List[SensitiveWord]:
        """鏍规嵁鏁忔劅绾у埆鑾峰彇鏁忔劅璇?""
        return self.db.query(SensitiveWord).filter(
            SensitiveWord.level == level,
            SensitiveWord.status == "active"
        ).order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """鎼滅储鏁忔劅璇?""
        query = self.db.query(SensitiveWord)

        # 鏁忔劅璇嶆悳绱?        if query_params.get("word"):
            query = query.filter(SensitiveWord.word.like(f"%{query_params['word']}%"))

        # 鍒嗙被杩囨护
        if query_params.get("category"):
            query = query.filter(SensitiveWord.category == query_params["category"])

        # 鏁忔劅绾у埆杩囨护
        if query_params.get("level"):
            query = query.filter(SensitiveWord.level == query_params["level"])

        # 鐘舵€佽繃婊?        if query_params.get("status"):
            query = query.filter(SensitiveWord.status == query_params["status"])

        # 缁熻鎬绘暟
        total = query.count()

        # 鍒嗛〉
        sensitive_words = query.order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

        return sensitive_words, total

    def create(self, sensitive_word: SensitiveWord) -> SensitiveWord:
        """鍒涘缓鏁忔劅璇?""
        self.db.add(sensitive_word)
        self.db.commit()
        self.db.refresh(sensitive_word)
        return sensitive_word

    def update(self, sensitive_word: SensitiveWord) -> SensitiveWord:
        """鏇存柊鏁忔劅璇?""
        self.db.commit()
        self.db.refresh(sensitive_word)
        return sensitive_word

    def delete(self, sensitive_word_id: str) -> bool:
        """鍒犻櫎鏁忔劅璇?""
        sensitive_word = self.get_by_id(sensitive_word_id)
        if sensitive_word:
            self.db.delete(sensitive_word)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """缁熻鏁忔劅璇嶆暟閲?""
        return self.db.query(SensitiveWord).count()

    def count_by_category(self, category: str) -> int:
        """鏍规嵁鍒嗙被缁熻鏁忔劅璇嶆暟閲?""
        return self.db.query(SensitiveWord).filter(SensitiveWord.category == category).count()

    def count_by_level(self, level: int) -> int:
        """鏍规嵁鏁忔劅绾у埆缁熻鏁忔劅璇嶆暟閲?""
        return self.db.query(SensitiveWord).filter(SensitiveWord.level == level).count()

    def get_all_active_words(self) -> List[str]:
        """鑾峰彇鎵€鏈夋縺娲荤殑鏁忔劅璇?""
        results = self.db.query(SensitiveWord.word).filter(
            SensitiveWord.status == "active"
        ).all()
        return [result[0] for result in results]
