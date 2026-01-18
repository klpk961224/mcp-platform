# -*- coding: utf-8 -*-
"""
认证服务

功能说明：
1. 用户登录
2. 用户登出
3. 密码验证
4. Token生成

使用示例：
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    result = auth_service.login(username="admin", password="123456")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any
from datetime import datetime

from common.database.models.user import User
from app.models.token import Token
from common.security.password import hash_password, verify_password
from common.security.jwt import create_access_token, create_refresh_token, verify_token
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository


class AuthService:
    """
    认证服务
    
    功能：
    - 用户登录验证
    - 密码验证
    - Token生成
    - 用户登出
    
    使用方法：
        auth_service = AuthService(db)
        result = auth_service.login(username="admin", password="123456")
    """
    
    def __init__(self, db: Session):
        """
        初始化认证服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)
    
    def register(self, username: str, password: str, email: str, 
                 phone: Optional[str] = None, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        用户注册
        
        Args:
            username: 用户名
            password: 密码
            email: 邮箱
            phone: 手机号（可选）
            tenant_id: 租户ID（可选）
        
        Returns:
            Dict: 注册结果，包含用户信息
        
        Raises:
            ValueError: 用户名已存在
            ValueError: 邮箱已存在
        """
        logger.info(f"用户注册尝试: username={username}, email={email}")
        
        # 检查用户名是否已存在
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            logger.warning(f"用户名已存在: username={username}")
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        existing_email = self.user_repo.get_by_email(email)
        if existing_email:
            logger.warning(f"邮箱已存在: email={email}")
            raise ValueError("邮箱已存在")
        
        # 如果没有提供租户ID，使用默认租户
        if not tenant_id:
            from common.database.models.tenant import Tenant
            default_tenant = self.db.query(Tenant).filter(Tenant.code == "default").first()
            if default_tenant:
                tenant_id = default_tenant.id
            else:
                raise ValueError("默认租户不存在")
        
        # 创建新用户
        import uuid
        user = User(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            username=username,
            password=hash_password(password),
            email=email,
            phone=phone,
            status="active"
        )
        
        # 保存用户
        self.user_repo.create(user)
        
        logger.info(f"用户注册成功: username={username}, user_id={user.id}")
        
        return {
            "message": "注册成功",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
    
    def login(self, username: str, password: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
            tenant_id: 租户ID（可选）
        
        Returns:
            Dict: 登录结果，包含用户信息和Token
        
        Raises:
            ValueError: 用户名或密码错误
            ValueError: 用户已被禁用
        """
        logger.info(f"用户登录尝试: username={username}, tenant_id={tenant_id}")
        
        # 查询用户
        user = self.user_repo.get_by_username(username)
        if not user:
            logger.warning(f"用户不存在: username={username}")
            raise ValueError("用户名或密码错误")
        
        # 验证密码
        if not verify_password(password, user.password):
            logger.warning(f"密码错误: username={username}")
            raise ValueError("用户名或密码错误")
        
        # 检查用户状态
        if user.status != "active":
            logger.warning(f"用户已被禁用: username={username}, status={user.status}")
            raise ValueError("用户已被禁用")
        
        # 检查租户
        if tenant_id and user.tenant_id != tenant_id:
            logger.warning(f"租户不匹配: username={username}, user_tenant={user.tenant_id}, request_tenant={tenant_id}")
            raise ValueError("租户不匹配")
        
        # 生成Token
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username, "tenant_id": user.tenant_id},
            expires_minutes=1440  # 24小时
        )
        
        refresh_token = create_refresh_token(
            data={"user_id": user.id},
            expires_days=30
        )
        
        # 保存Token到数据库
        from datetime import timedelta
        
        self.token_repo.create_token(
            user_id=user.id,
            token_type="access",
            token_hash=access_token,
            expires_at=datetime.now() + timedelta(hours=24)  # 24小时后过期
        )
        
        self.token_repo.create_token(
            user_id=user.id,
            token_type="refresh",
            token_hash=refresh_token,
            expires_at=datetime.now() + timedelta(days=30)  # 30天后过期
        )
        
        # 更新最后登录时间
        user.last_login_at = datetime.now()
        self.user_repo.update(user)
        
        logger.info(f"用户登录成功: username={username}, user_id={user.id}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 86400,  # 24小时
            "user_info": user.to_dict()
        }
    
    def logout(self, user_id: str) -> bool:
        """
        用户登出
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 登出是否成功
        """
        logger.info(f"用户登出: user_id={user_id}")
        
        # 吊销所有Token
        self.token_repo.revoke_all_tokens(user_id)
        
        logger.info(f"用户登出成功: user_id={user_id}")
        return True
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        刷新Token
        
        Args:
            refresh_token: 刷新Token
        
        Returns:
            Dict: 新的访问Token
        
        Raises:
            ValueError: Token无效或已过期
        """
        logger.info("刷新Token请求")
        
        # 验证Token
        payload = verify_token(refresh_token)
        if not payload:
            raise ValueError("Token无效或已过期")
        
        # 从sub字段获取user_id（JWT标准使用sub表示subject）
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token中缺少用户ID")
        
        # 生成新的访问Token
        new_access_token = create_access_token(
            data={"user_id": user_id},
            expires_minutes=1440
        )
        
        logger.info(f"刷新Token成功: user_id={user_id}")
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 86400
        }

