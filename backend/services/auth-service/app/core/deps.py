"""
渚濊禆娉ㄥ叆妯″潡

鍔熻兘璇存槑锛?1. 鎻愪緵鏁版嵁搴撲細璇濅緷璧?2. 鎻愪緵褰撳墠鐢ㄦ埛渚濊禆
3. 鎻愪緵鏉冮檺鏍￠獙渚濊禆

浣跨敤绀轰緥锛?    from app.core.deps import get_db, get_current_user

    @router.get("/users")
    async def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
        return users
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Generator
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from common.database import get_session
from common.security import verify_token
from common.database.connection import datasource_manager


def get_db() -> Generator[Session, None, None]:
    """
    鑾峰彇鏁版嵁搴撲細璇濓紙鐢熸垚鍣ㄥ嚱鏁帮紝鐢ㄤ簬FastAPI渚濊禆娉ㄥ叆锛?
    Returns:
        Generator[Session, None, None]: 鏁版嵁搴撲細璇濈敓鎴愬櫒

    浣跨敤绀轰緥锛?        @router.get("/users")
        async def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    session = None
    try:
        session = datasource_manager.get_session('mysql')
        yield session
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()


async def get_current_user(
    token: str = Depends(lambda: None),
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    鑾峰彇褰撳墠鐢ㄦ埛
    
    Args:
        token: JWT Token
        db: 鏁版嵁搴撲細璇?    
    Returns:
        Optional[dict]: 鐢ㄦ埛淇℃伅
    
    浣跨敤绀轰緥锛?        @router.get("/profile")
        async def get_profile(current_user = Depends(get_current_user)):
            return current_user
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="鏈彁渚涜璇乀oken"
        )
    
    # 楠岃瘉Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token鏃犳晥鎴栧凡杩囨湡"
        )
    
    # 浠庢暟鎹簱鑾峰彇鐢ㄦ埛淇℃伅
    # user = db.query(User).filter(User.id == payload.get("user_id")).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="鐢ㄦ埛涓嶅瓨鍦?
    #     )
    
    return payload


async def get_current_active_user(
    current_user = Depends(get_current_user)
) -> dict:
    """
    鑾峰彇褰撳墠娲昏穬鐢ㄦ埛
    
    Args:
        current_user: 褰撳墠鐢ㄦ埛
    
    Returns:
        dict: 鐢ㄦ埛淇℃伅
    
    浣跨敤绀轰緥锛?        @router.get("/profile")
        async def get_profile(current_user = Depends(get_current_active_user)):
            return current_user
    """
    if current_user.get("status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="鐢ㄦ埛宸茶禁用"
        )
    
    return current_user
