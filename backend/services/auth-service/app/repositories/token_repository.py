# -*- coding: utf-8 -*-
"""
Token数据访问层

功能说明：
1. Token CRUD操作
2. Token查询操作
3. Token清理操作

使用示例：
    from app.repositories.token_repository import TokenRepository
    
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
    Token数据访问层
    
    功能：
    - Token CRUD操作
    - Token查询操作
    - Token清理操作
    
    使用方法：
        token_repo = TokenRepository(db)
        token = token_repo.get_by_token_hash("hash")
    """
    
    def __init__(self, db: Session):
        """
        初始化Token数据访问层
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create_token(self, user_id: str, token_type: str, token_hash: str, expires_at: Optional[datetime] = None) -> Token:
        """
        创建Token
        
        Args:
            user_id: 用户ID
            token_type: Token类型
            token_hash: Token哈希
            expires_at: 过期时间
        
        Returns:
            Token: 创建的Token对象
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
        根据ID获取Token
        
        Args:
            token_id: Token ID
        
        Returns:
            Optional[Token]: Token对象，不存在返回None
        """
        return self.db.query(Token).filter(Token.id == token_id).first()
    
    def get_by_token_hash(self, token_hash: str) -> Optional[Token]:
        """
        根据Token哈希获取Token
        
        Args:
            token_hash: Token哈希
        
        Returns:
            Optional[Token]: Token对象，不存在返回None
        """
        return self.db.query(Token).filter(Token.token_hash == token_hash).first()
    
    def get_by_user_id(self, user_id: str) -> List[Token]:
        """
        根据用户ID获取所有Token
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Token]: Token列表
        """
        return self.db.query(Token).filter(Token.user_id == user_id).all()
    
    def get_by_type(self, token_type: str, page: int = 1, page_size: int = 10) -> List[Token]:
        """
        根据Token类型获取Token列表
        
        Args:
            token_type: Token类型
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Token]: Token列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Token).filter(Token.token_type == token_type).offset(offset).limit(page_size).all()
    
    def get_all(self, page: int = 1, page_size: int = 10) -> List[Token]:
        """
        获取所有Token
        
        Args:
            page: 页码
            page_size: 每页数量
        
        Returns:
            List[Token]: Token列表
        """
        offset = (page - 1) * page_size
        return self.db.query(Token).offset(offset).limit(page_size).all()
    
    def update(self, token: Token) -> Token:
        """
        更新Token
        
        Args:
            token: Token对象
        
        Returns:
            Token: 更新后的Token对象
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
            bool: 删除是否成功
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
        获取所有过期的Token
        
        Returns:
            List[Token]: 过期的Token列表
        """
        return self.db.query(Token).filter(Token.expires_at < datetime.now()).all()
    
    def get_revoked_tokens(self) -> List[Token]:
        """
        获取所有已吊销的Token
        
        Returns:
            List[Token]: 已吊销的Token列表
        """
        return self.db.query(Token).filter(Token.is_revoked == True).all()
    
    def count_by_user(self, user_id: str) -> int:
        """
        统计用户的Token数量
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: Token数量
        """
        return self.db.query(Token).filter(Token.user_id == user_id).count()
    
    def count_by_type(self, token_type: str) -> int:
        """
        统计Token类型的数量
        
        Args:
            token_type: Token类型
        
        Returns:
            int: Token数量
        """
        return self.db.query(Token).filter(Token.token_type == token_type).count()
    
    def count_all(self) -> int:
        """
        统计所有Token数量
        
        Returns:
            int: Token数量
        """
        return self.db.query(Token).count()
    
    def revoke_all_tokens(self, user_id: str) -> int:
        """
        吊销用户的所有Token
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 吊销的Token数量
        """
        logger.info(f"吊销用户所有Token: user_id={user_id}")
        tokens = self.get_by_user_id(user_id)
        count = 0
        for token in tokens:
            if not token.is_revoked:
                token.revoke()
                count += 1
        self.db.commit()
        logger.info(f"吊销了 {count} 个Token: user_id={user_id}")
        return count
    
    def revoke_token(self, token_id: str) -> bool:
        """
        吊销Token
        
        Args:
            token_id: Token ID
        
        Returns:
            bool: 吊销是否成功
        """
        logger.info(f"吊销Token: token_id={token_id}")
        token = self.get_by_id(token_id)
        if not token:
            return False
        
        token.revoke()
        self.db.commit()
        return True
    
    def delete_expired_tokens(self) -> int:
        """
        删除所有过期的Token
        
        Returns:
            int: 删除的Token数量
        """
        logger.info("删除所有过期的Token")
        expired_tokens = self.get_expired_tokens()
        count = len(expired_tokens)
        for token in expired_tokens:
            self.db.delete(token)
        self.db.commit()
        logger.info(f"删除了 {count} 个过期Token")
        return count