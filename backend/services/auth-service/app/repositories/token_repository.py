# -*- coding: utf-8 -*-
"""
Token鏁版嵁璁块棶灞?
鍔熻兘璇存槑锛?1. Token CRUD鎿嶄綔
2. Token鏌ヨ鎿嶄綔
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
    - Token鏌ヨ鎿嶄綔
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
        鍒涘缓Token
        
        Args:
            user_id: 鐢ㄦ埛ID
            token_type: Token绫诲瀷
            token_hash: Token鍝堝笇
            expires_at: 杩囨湡鏃堕棿
        
        Returns:
            Token: 鍒涘缓鐨凾oken瀵硅薄
        """
        logger.info(f"鍒涘缓Token: user_id={user_id}, token_type={token_type}")
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
        鏍规嵁ID鑾峰彇Token
        
        Args:
            token_id: Token ID
        
        Returns:
            Optional[Token]: Token瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Token).filter(Token.id == token_id).first()
    
    def get_by_token_hash(self, token_hash: str) -> Optional[Token]:
        """
        鏍规嵁Token鍝堝笇鑾峰彇Token
        
        Args:
            token_hash: Token鍝堝笇
        
        Returns:
            Optional[Token]: Token瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.db.query(Token).filter(Token.token_hash == token_hash).first()
    
    def get_by_user_id(self, user_id: str) -> List[Token]:
        """
        鏍规嵁鐢ㄦ埛ID鑾峰彇鎵€鏈塗oken
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            List[Token]: Token鍒楄〃
        """
        return self.db.query(Token).filter(Token.user_id == user_id).all()
    
    def get_by_type(self, token_type: str, page: int = 1, page_size: int = 10) -> List[Token]:
        """
        鏍规嵁Token绫诲瀷鑾峰彇Token鍒楄〃
        
        Args:
            token_type: Token绫诲瀷
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
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
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[Token]: Token鍒楄〃
        """
        offset = (page - 1) * page_size
        return self.db.query(Token).offset(offset).limit(page_size).all()
    
    def update(self, token: Token) -> Token:
        """
        鏇存柊Token
        
        Args:
            token: Token瀵硅薄
        
        Returns:
            Token: 鏇存柊鍚庣殑Token瀵硅薄
        """
        logger.info(f"鏇存柊Token: token_id={token.id}")
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def delete(self, token_id: str) -> bool:
        """
        鍒犻櫎Token
        
        Args:
            token_id: Token ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎Token: token_id={token_id}")
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
        缁熻鐢ㄦ埛鐨凾oken鏁伴噺
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            int: Token鏁伴噺
        """
        return self.db.query(Token).filter(Token.user_id == user_id).count()
    
    def count_by_type(self, token_type: str) -> int:
        """
        缁熻Token绫诲瀷鐨勬暟閲?        
        Args:
            token_type: Token绫诲瀷
        
        Returns:
            int: Token鏁伴噺
        """
        return self.db.query(Token).filter(Token.token_type == token_type).count()
    
    def count_all(self) -> int:
        """
        缁熻鎵€鏈塗oken鏁伴噺
        
        Returns:
            int: Token鏁伴噺
        """
        return self.db.query(Token).count()
    
    def revoke_all_tokens(self, user_id: str) -> int:
        """
        鍚婇攢鐢ㄦ埛鐨勬墍鏈塗oken
        
        Args:
            user_id: 鐢ㄦ埛ID
        
        Returns:
            int: 鍚婇攢鐨凾oken鏁伴噺
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
        鍒犻櫎鎵€鏈夎繃鏈熺殑Token
        
        Returns:
            int: 鍒犻櫎鐨凾oken鏁伴噺
        """
        logger.info("鍒犻櫎鎵€鏈夎繃鏈熺殑Token")
        expired_tokens = self.get_expired_tokens()
        count = len(expired_tokens)
        for token in expired_tokens:
            self.db.delete(token)
        self.db.commit()
        logger.info(f"鍒犻櫎浜?{count} 涓繃鏈烼oken")
        return count
