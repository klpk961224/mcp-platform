# -*- coding: utf-8 -*-
"""
Token妯″瀷

鍔熻兘璇存槑锛?1. 璁块棶Token绠＄悊
2. 鍒锋柊Token绠＄悊
3. Token榛戝悕鍗?
浣跨敤绀轰緥锛?    from app.models.token import Token
    
    # 鍒涘缓Token
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
    Token妯″瀷
    
    鍔熻兘锛?    - 璁块棶Token绠＄悊
    - 鍒锋柊Token绠＄悊
    - Token榛戝悕鍗?    
    灞炴€ц鏄庯細
    - id: Token ID锛堜富閿級
    - user_id: 鐢ㄦ埛ID锛堝閿級
    - token_type: Token绫诲瀷锛坅ccess/refresh锛?    - token_hash: Token鍝堝笇
    - expires_at: 杩囨湡鏃堕棿
    - is_revoked: 鏄惁宸插悐閿€
    - revoked_at: 鍚婇攢鏃堕棿
    - created_at: 鍒涘缓鏃堕棿
    """
    
    __tablename__ = "tokens"
    
    # 鍩烘湰淇℃伅
    user_id = Column(String(64), nullable=False, index=True, comment="鐢ㄦ埛ID")
    token_type = Column(String(20), nullable=False, comment="Token绫诲瀷")
    token_hash = Column(String(255), nullable=False, unique=True, index=True, comment="Token鍝堝笇")
    
    # 杩囨湡淇℃伅
    expires_at = Column(DateTime, nullable=False, comment="杩囨湡鏃堕棿")
    
    # 鍚婇攢淇℃伅
    is_revoked = Column(Boolean, nullable=False, default=False, comment="鏄惁宸插悐閿€")
    revoked_at = Column(DateTime, nullable=True, comment="鍚婇攢鏃堕棿")
    
    def __repr__(self):
        return f"<Token(id={self.id}, user_id={self.user_id}, token_type={self.token_type})>"
    
    def is_expired(self):
        """妫€鏌oken鏄惁杩囨湡"""
        return datetime.now() > self.expires_at
    
    def is_valid(self):
        """妫€鏌oken鏄惁鏈夋晥"""
        return not self.is_revoked and not self.is_expired()
    
    def revoke(self):
        """鍚婇攢Token"""
        self.is_revoked = True
        self.revoked_at = datetime.now()
