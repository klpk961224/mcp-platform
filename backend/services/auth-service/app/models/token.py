# -*- coding: utf-8 -*-
"""
Token模型

功能说明：
1. 访问Token管理
2. 刷新Token管理
3. Token黑名单

使用示例：
    from app.models.token import Token
    
    # 创建Token
    token = Token(
        user_id="123",
        token_type="access",
        expires_at=datetime.now() + timedelta(hours=2)
    )
"""

from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime, timedelta

from common.database.base import BaseModel


class Token(BaseModel):
    """
    Token模型
    
    功能：
    - 访问Token管理
    - 刷新Token管理
    - Token黑名单
    
    属性说明：
    - id: Token ID（主键）
    - user_id: 用户ID（外键）
    - token_type: Token类型（access/refresh）
    - token_hash: Token哈希
    - expires_at: 过期时间
    - is_revoked: 是否已吊销
    - revoked_at: 吊销时间
    - created_at: 创建时间
    """
    
    __tablename__ = "tokens"
    
    # 基本信息
    user_id = Column(String(64), nullable=False, index=True, comment="用户ID")
    token_type = Column(String(20), nullable=False, comment="Token类型")
    token_hash = Column(String(255), nullable=False, unique=True, index=True, comment="Token哈希")
    
    # 过期信息
    expires_at = Column(DateTime, nullable=False, comment="过期时间")
    
    # 吊销信息
    is_revoked = Column(Boolean, nullable=False, default=False, comment="是否已吊销")
    revoked_at = Column(DateTime, nullable=True, comment="吊销时间")
    
    def __repr__(self):
        return f"<Token(id={self.id}, user_id={self.user_id}, token_type={self.token_type})>"
    
    def is_expired(self):
        """检查Token是否过期"""
        return datetime.now() > self.expires_at
    
    def is_valid(self):
        """检查Token是否有效"""
        return not self.is_revoked and not self.is_expired()
    
    def revoke(self):
        """吊销Token"""
        self.is_revoked = True
        self.revoked_at = datetime.now()