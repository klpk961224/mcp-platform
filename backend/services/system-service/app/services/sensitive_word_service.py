"""
敏感词Service

提供敏感词业务逻辑层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from common.database.models.sensitive_word import SensitiveWord
from app.repositories.sensitive_word_repository import SensitiveWordRepository


class SensitiveWordService:
    """敏感词Service"""

    # 敏感级别常量
    LEVEL_LOW = 1  # 低
    LEVEL_MEDIUM = 2  # 中
    LEVEL_HIGH = 3  # 高
    LEVEL_CRITICAL = 4  # 严重

    # 分类常量
    CATEGORY_POLITICAL = "political"  # 政治
    CATEGORY_PORN = "porn"  # 色情
    CATEGORY_VIOLENCE = "violence"  # 暴力
    CATEGORY_AD = "ad"  # 广告
    CATEGORY_OTHER = "other"  # 其他

    # 状态常量
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    def __init__(self, db: Session):
        self.db = db
        self.repository = SensitiveWordRepository(db)

    def get_sensitive_word_by_id(self, sensitive_word_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取敏感词"""
        sensitive_word = self.repository.get_by_id(sensitive_word_id)
        if not sensitive_word:
            return None
        return self._to_dict(sensitive_word)

    def get_sensitive_word_by_word(self, word: str) -> Optional[Dict[str, Any]]:
        """根据敏感词获取"""
        sensitive_word = self.repository.get_by_word(word)
        if not sensitive_word:
            return None
        return self._to_dict(sensitive_word)

    def get_all_sensitive_words(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """获取所有敏感词"""
        sensitive_words = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {
            "items": [self._to_dict(sw) for sw in sensitive_words],
            "total": total
        }

    def get_sensitive_words_by_category(self, category: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """根据分类获取敏感词"""
        sensitive_words = self.repository.get_by_category(category, skip=skip, limit=limit)
        total = self.repository.count_by_category(category)
        return {
            "items": [self._to_dict(sw) for sw in sensitive_words],
            "total": total
        }

    def get_sensitive_words_by_level(self, level: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """根据敏感级别获取敏感词"""
        sensitive_words = self.repository.get_by_level(level, skip=skip, limit=limit)
        total = self.repository.count_by_level(level)
        return {
            "items": [self._to_dict(sw) for sw in sensitive_words],
            "total": total
        }

    def search_sensitive_words(
        self,
        query_params: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """搜索敏感词"""
        sensitive_words, total = self.repository.search(query_params, skip=skip, limit=limit)
        return {
            "items": [self._to_dict(sw) for sw in sensitive_words],
            "total": total
        }

    def create_sensitive_word(
        self,
        word: str,
        category: str,
        level: int = LEVEL_LOW,
        replacement: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """创建敏感词"""
        # 检查敏感词是否已存在
        existing = self.repository.get_by_word(word)
        if existing:
            raise ValueError(f"敏感词 {word} 已存在")

        # 创建敏感词
        sensitive_word = SensitiveWord(
            word=word,
            category=category,
            level=level,
            replacement=replacement,
            description=description,
            status=self.STATUS_ACTIVE
        )

        sensitive_word = self.repository.create(sensitive_word)
        return self._to_dict(sensitive_word)

    def update_sensitive_word(
        self,
        sensitive_word_id: str,
        word: Optional[str] = None,
        category: Optional[str] = None,
        level: Optional[int] = None,
        replacement: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """更新敏感词"""
        sensitive_word = self.repository.get_by_id(sensitive_word_id)
        if not sensitive_word:
            return None

        # 更新字段
        if word is not None:
            sensitive_word.word = word
        if category is not None:
            sensitive_word.category = category
        if level is not None:
            sensitive_word.level = level
        if replacement is not None:
            sensitive_word.replacement = replacement
        if description is not None:
            sensitive_word.description = description
        if status is not None:
            sensitive_word.status = status

        sensitive_word = self.repository.update(sensitive_word)
        return self._to_dict(sensitive_word)

    def delete_sensitive_word(self, sensitive_word_id: str) -> bool:
        """删除敏感词"""
        return self.repository.delete(sensitive_word_id)

    def get_all_active_words(self) -> List[str]:
        """获取所有激活的敏感词"""
        return self.repository.get_all_active_words()

    def check_text(self, text: str) -> Dict[str, Any]:
        """
        检查文本是否包含敏感词

        Args:
            text: 待检查的文本

        Returns:
            Dict: 包含检查结果和敏感词列表
        """
        active_words = self.get_all_active_words()
        found_words = []

        for word in active_words:
            if word in text:
                found_words.append(word)

        return {
            "has_sensitive": len(found_words) > 0,
            "sensitive_words": found_words,
            "count": len(found_words)
        }

    def filter_text(self, text: str) -> str:
        """
        过滤文本中的敏感词

        Args:
            text: 待过滤的文本

        Returns:
            str: 过滤后的文本
        """
        active_words = self.get_all_active_words()
        filtered_text = text

        for word in active_words:
            sensitive_word = self.repository.get_by_word(word)
            if sensitive_word and sensitive_word.replacement:
                # 使用替换词
                filtered_text = filtered_text.replace(word, sensitive_word.replacement)
            else:
                # 使用星号替换
                filtered_text = filtered_text.replace(word, "*" * len(word))

        return filtered_text

    def get_statistics(self) -> Dict[str, Any]:
        """获取敏感词统计信息"""
        total = self.repository.count()

        # 按分类统计
        category_stats = {}
        for category in [self.CATEGORY_POLITICAL, self.CATEGORY_PORN, self.CATEGORY_VIOLENCE, self.CATEGORY_AD, self.CATEGORY_OTHER]:
            category_stats[category] = self.repository.count_by_category(category)

        # 按级别统计
        level_stats = {}
        for level in [self.LEVEL_LOW, self.LEVEL_MEDIUM, self.LEVEL_HIGH, self.LEVEL_CRITICAL]:
            level_stats[level] = self.repository.count_by_level(level)

        # 按状态统计
        active_count = self.repository.search({"status": self.STATUS_ACTIVE}, skip=0, limit=999999)[1]
        inactive_count = self.repository.search({"status": self.STATUS_INACTIVE}, skip=0, limit=999999)[1]

        return {
            "total": total,
            "by_category": category_stats,
            "by_level": level_stats,
            "by_status": {
                "active": active_count,
                "inactive": inactive_count
            }
        }

    def _to_dict(self, sensitive_word: SensitiveWord) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": sensitive_word.id,
            "word": sensitive_word.word,
            "category": sensitive_word.category,
            "level": sensitive_word.level,
            "replacement": sensitive_word.replacement,
            "description": sensitive_word.description,
            "status": sensitive_word.status,
            "created_at": sensitive_word.created_at.isoformat() if sensitive_word.created_at else None,
            "updated_at": sensitive_word.updated_at.isoformat() if sensitive_word.updated_at else None
        }