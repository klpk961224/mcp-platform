# -*- coding: utf-8 -*-
"""
Token鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. Token CRUD鎿嶄綔
2. Token查询鎿嶄綔
3. Token娓呯悊鎿嶄綔

浣跨敤绀轰緥锛?    from app.repositories.token_repository import TokenRepository
    
    token_repo = TokenRepository(db)
    token = token_repo.get_by_token_hash("hash")
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from loguru import logger

from app.models.token import Token


class TokenRepository:
    """
    Token鏁版嵁璁块棶灞?    
    鍔熻兘锛?    - Token CRUD鎿嶄綔
    - Token查询鎿嶄綔
    - Token娓呯悊鎿嶄綔
    
    浣跨敤鏂规硶锛?        token_repo = TokenRepository(db)
        token = token_repo.get_by_token_hash("hash")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖朤oken鏁版嵁璁块棶灞?        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
    
    def create_token(self, user_id: str, token_type: str, token_hash: str, expires_at: Optional[datetime] = None) -> Token:
        """
        创建Token
        
        Args:
            user_id: 用户ID
            token_type: Token类型
            token_hash: Token鍝堝笇
            expires_at: 杩囨湡鏃堕棿
        
        Returns:
            Token: 创建鐨凾oken瀵硅薄
        """
        logger.info(f"创建Token: user_id={user_id}, token_type={token_type}")
        token = Token(
            user_id=user_id,
            token_type=token_type,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def get_by_id(self, token_id: str) -> Optional[Token]:
        """
        根据ID鑾峰彇Token
        
        Args:
            token_id: Token ID
        
        Returns:
            Optional[Token]: Token瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Token).filter(Token.id == token_id).first()
    
    def get_by_token_hash(self, token_hash: str) -> Optional[Token]:
        """
        根据Token鍝堝笇鑾峰彇Token
        
        Args:
            token_hash: Token鍝堝笇
        
        Returns:
            Optional[Token]: Token瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Token).filter(Token.token_hash == token_hash).first()
    
    def get_by_user_id(self, user_id: str) -> List[Token]:
        """
        根据用户ID鑾峰彇鎵€鏈塗oken
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Token]: Token鍒楄〃
        """
        return self.db.query(Token).filter(Token.user_id == user_id).all()
    
    def get_by_type(self, token_type: str, page: int = 1, page_size: int = 10) -> List[Token]:
        """
        根据Token类型鑾峰彇Token鍒楄〃
        
        Args:
            token_type: Token类型
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Token]: Token鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Token).filter(Token.token_type == token_type).offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Token]:
        """
        鑾峰彇鎵€鏈塗oken
        
        Args:
            page: 椤电爜
            page_size: 姣忛〉数量
        
        Returns:
            List[Token]: Token鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Token).offset(offset).limit(page_size).all()
    
    def update(self, token: Token) -> Token:
        """
        更新Token
        
        Args:
            token: Token瀵硅薄
        
        Returns:
            Token: 更新鍚庣殑Token瀵硅薄
        """
        logger.info(f"更新Token: token_id={token.id}")
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def delete(self, token_id: str) -> bool:
        """
        删除Token
        
        Args:
            token_id: Token ID
        
        Returns:
            bool: 删除鏄惁鎴愬姛
        """
        logger.info(f"删除Token: token_id={token_id}")
        token = self.get_by_id(token_id)
        if not token:
            return False
        
        self.db.delete(token)
        self.db.commit()
        return True
    
    def get_expired_tokens(self) -> List[Token]:
        """
        鑾峰彇鎵€鏈夎繃鏈熺殑Token
        
        Returns:
            List[Token]: 杩囨湡鐨凾oken鍒楄〃
        """
        return self.db.query(Token).filter(Token.expires_at < datetime.now()).all()
    
    def get_revoked_tokens(self) -> List[Token]:
        """
        鑾峰彇鎵€鏈夊凡鍚婇攢鐨凾oken
        
        Returns:
            List[Token]: 宸插悐閿€鐨凾oken鍒楄〃
        """
        return self.db.query(Token).filter(Token.is_revoked == True).all()
    
    def count_by_user(self, user_id: str) -> int:
        """
        缁熻鐢ㄦ埛鐨凾oken数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: Token数量
        """
        return self.db.query(Token).filter(Token.user_id == user_id).count()
    
    def count_by_type(self, token_type: str) -> int:
        """
        缁熻Token类型鐨勬暟閲?        
        Args:
            token_type: Token类型
        
        Returns:
            int: Token数量
        """
        return self.db.query(Token).filter(Token.token_type == token_type).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈塗oken数量
        
        Returns:
            int: Token数量
        """
        return self.db.query(Token).count()
    
    def revoke_all_tokens(self, user_id: str) -> int:
        """
        鍚婇攢鐢ㄦ埛鐨勬墍鏈塗oken
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 鍚婇攢鐨凾oken数量
        """
        logger.info(f"鍚婇攢鐢ㄦ埛鎵€鏈塗oken: user_id={user_id}")
        tokens = self.get_by_user_id(user_id)
        count = 0
        for token in tokens:
            if not token.is_revoked:
                token.revoke()
                count += 1
        self.db.commit()
        logger.info(f"鍚婇攢浜?{count} 涓猅oken: user_id={user_id}")
        return count
    
    def revoke_token(self, token_id: str) -> bool:
        """
        鍚婇攢Token
        
        Args:
            token_id: Token ID
        
        Returns:
            bool: 鍚婇攢鏄惁鎴愬姛
        """
        logger.info(f"鍚婇攢Token: token_id={token_id}")
        token = self.get_by_id(token_id)
        if not token:
            return False
        
        token.revoke()
        self.db.commit()
        return True
    
    def delete_expired_tokens(self) -> int:
        """
        删除鎵€鏈夎繃鏈熺殑Token
        
        Returns:
            int: 删除鐨凾oken数量
        """
        logger.info("删除鎵€鏈夎繃鏈熺殑Token")
        expired_tokens = self.get_expired_tokens()
        count = len(expired_tokens)
        for token in expired_tokens:
            self.db.delete(token)
        self.db.commit()
        logger.info(f"删除浜?{count} 涓繃鏈烼oken")
        return count
