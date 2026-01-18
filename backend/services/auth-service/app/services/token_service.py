# -*- coding: utf-8 -*-
"""
Token绠＄悊鏈嶅姟

鍔熻兘璇存槑锛?1. Token鐢熸垚
2. Token楠岃瘉
3. Token鍚婇攢
4. Token娓呯悊

浣跨敤绀轰緥锛?    from app.services.token_service import TokenService
    
    token_service = TokenService(db)
    token_service.create_token(user_id="123", token_type="access")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional
from datetime import datetime

from app.models.token import Token
from app.repositories.token_repository import TokenRepository


class TokenService:
    """
    Token绠＄悊鏈嶅姟
    
    鍔熻兘锛?    - Token鐢熸垚
    - Token楠岃瘉
    - Token鍚婇攢
    - Token娓呯悊
    
    浣跨敤鏂规硶锛?        token_service = TokenService(db)
        token = token_service.create_token(user_id="123", token_type="access")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖朤oken鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.token_repo = TokenRepository(db)
    
    def create_token(self, user_id: str, token_type: str, token_hash: str, expires_at: Optional[datetime] = None) -> Token:
        """
        创建Token
        
        Args:
            user_id: 用户ID
            token_type: Token类型
            token_hash: Token鍝堝笇
            expires_at: 杩囨湡鏃堕棿
        
        Returns:
            Token: Token瀵硅薄
        """
        logger.info(f"创建Token: user_id={user_id}, token_type={token_type}")
        
        token = self.token_repo.create_token(
            user_id=user_id,
            token_type=token_type,
            token_hash=token_hash,
            expires_at=expires_at
        )
        
        return token
    
    def revoke_token(self, token_hash: str) -> bool:
        """
        鍚婇攢Token
        
        Args:
            token_hash: Token鍝堝笇
        
        Returns:
            bool: 鍚婇攢鏄惁鎴愬姛
        """
        logger.info(f"鍚婇攢Token: token_hash={token_hash[:20]}...")
        
        token = self.token_repo.get_by_token_hash(token_hash)
        if not token:
            return False
        
        token.revoke()
        self.token_repo.update(token)
        
        return True
    
    def revoke_all_tokens(self, user_id: str) -> int:
        """
        鍚婇攢鐢ㄦ埛鎵€鏈塗oken
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 鍚婇攢鐨凾oken数量
        """
        logger.info(f"鍚婇攢鐢ㄦ埛鎵€鏈塗oken: user_id={user_id}")
        
        tokens = self.token_repo.get_by_user_id(user_id)
        count = 0
        for token in tokens:
            token.revoke()
            self.token_repo.update(token)
            count += 1
        
        return count
    
    def clean_expired_tokens(self) -> int:
        """
        娓呯悊杩囨湡Token
        
        Returns:
            int: 娓呯悊鐨凾oken数量
        """
        logger.info("娓呯悊杩囨湡Token")
        
        tokens = self.token_repo.get_expired_tokens()
        count = 0
        for token in tokens:
            self.token_repo.delete(token.id)
            count += 1
        
        logger.info(f"娓呯悊杩囨湡Token瀹屾垚: 娓呯悊浜唟count}涓猅oken")
        return count
