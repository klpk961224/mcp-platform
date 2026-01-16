# -*- coding: utf-8 -*-
"""
Token管理服务

功能说明：
1. Token生成
2. Token验证
3. Token吊销
4. Token清理

使用示例：
    from app.services.token_service import TokenService
    
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
    Token管理服务
    
    功能：
    - Token生成
    - Token验证
    - Token吊销
    - Token清理
    
    使用方法：
        token_service = TokenService(db)
        token = token_service.create_token(user_id="123", token_type="access")
    """
    
    def __init__(self, db: Session):
        """
        初始化Token服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.token_repo = TokenRepository(db)
    
    def create_token(self, user_id: str, token_type: str, token_hash: str, expires_at: Optional[datetime] = None) -> Token:
        """
        创建Token
        
        Args:
            user_id: 用户ID
            token_type: Token类型
            token_hash: Token哈希
            expires_at: 过期时间
        
        Returns:
            Token: Token对象
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
        吊销Token
        
        Args:
            token_hash: Token哈希
        
        Returns:
            bool: 吊销是否成功
        """
        logger.info(f"吊销Token: token_hash={token_hash[:20]}...")
        
        token = self.token_repo.get_by_token_hash(token_hash)
        if not token:
            return False
        
        token.revoke()
        self.token_repo.update(token)
        
        return True
    
    def revoke_all_tokens(self, user_id: str) -> int:
        """
        吊销用户所有Token
        
        Args:
            user_id: 用户ID
        
        Returns:
            int: 吊销的Token数量
        """
        logger.info(f"吊销用户所有Token: user_id={user_id}")
        
        tokens = self.token_repo.get_by_user_id(user_id)
        count = 0
        for token in tokens:
            token.revoke()
            self.token_repo.update(token)
            count += 1
        
        return count
    
    def clean_expired_tokens(self) -> int:
        """
        清理过期Token
        
        Returns:
            int: 清理的Token数量
        """
        logger.info("清理过期Token")
        
        tokens = self.token_repo.get_expired_tokens()
        count = 0
        for token in tokens:
            self.token_repo.delete(token.id)
            count += 1
        
        logger.info(f"清理过期Token完成: 清理了{count}个Token")
        return count