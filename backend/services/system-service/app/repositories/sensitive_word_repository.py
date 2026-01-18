"""
敏感词Repository

提供敏感词数据访问层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from common.database.models.sensitive_word import SensitiveWord


class SensitiveWordRepository:
    """敏感词Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sensitive_word_id: str) -> Optional[SensitiveWord]:
        """根据ID获取敏感词"""
        return self.db.query(SensitiveWord).filter(SensitiveWord.id == sensitive_word_id).first()

    def get_by_word(self, word: str) -> Optional[SensitiveWord]:
        """根据敏感词获取"""
        return self.db.query(SensitiveWord).filter(SensitiveWord.word == word).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SensitiveWord]:
        """获取所有敏感词"""
        return self.db.query(SensitiveWord).order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[SensitiveWord]:
        """根据分类获取敏感词"""
        return self.db.query(SensitiveWord).filter(
            SensitiveWord.category == category,
            SensitiveWord.status == "active"
        ).order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

    def get_by_level(self, level: int, skip: int = 0, limit: int = 100) -> List[SensitiveWord]:
        """根据敏感级别获取敏感词"""
        return self.db.query(SensitiveWord).filter(
            SensitiveWord.level == level,
            SensitiveWord.status == "active"
        ).order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """搜索敏感词"""
        query = self.db.query(SensitiveWord)

        # 敏感词搜索
        if query_params.get("word"):
            query = query.filter(SensitiveWord.word.like(f"%{query_params['word']}%"))

        # 分类过滤
        if query_params.get("category"):
            query = query.filter(SensitiveWord.category == query_params["category"])

        # 敏感级别过滤
        if query_params.get("level"):
            query = query.filter(SensitiveWord.level == query_params["level"])

        # 状态过滤
        if query_params.get("status"):
            query = query.filter(SensitiveWord.status == query_params["status"])

        # 统计总数
        total = query.count()

        # 分页
        sensitive_words = query.order_by(SensitiveWord.level.desc()).offset(skip).limit(limit).all()

        return sensitive_words, total

    def create(self, sensitive_word: SensitiveWord) -> SensitiveWord:
        """创建敏感词"""
        self.db.add(sensitive_word)
        self.db.commit()
        self.db.refresh(sensitive_word)
        return sensitive_word

    def update(self, sensitive_word: SensitiveWord) -> SensitiveWord:
        """更新敏感词"""
        self.db.commit()
        self.db.refresh(sensitive_word)
        return sensitive_word

    def delete(self, sensitive_word_id: str) -> bool:
        """删除敏感词"""
        sensitive_word = self.get_by_id(sensitive_word_id)
        if sensitive_word:
            self.db.delete(sensitive_word)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """统计敏感词数量"""
        return self.db.query(SensitiveWord).count()

    def count_by_category(self, category: str) -> int:
        """根据分类统计敏感词数量"""
        return self.db.query(SensitiveWord).filter(SensitiveWord.category == category).count()

    def count_by_level(self, level: int) -> int:
        """根据敏感级别统计敏感词数量"""
        return self.db.query(SensitiveWord).filter(SensitiveWord.level == level).count()

    def get_all_active_words(self) -> List[str]:
        """获取所有激活的敏感词"""
        results = self.db.query(SensitiveWord.word).filter(
            SensitiveWord.status == "active"
        ).all()
        return [result[0] for result in results]