"""
渚濊禆娉ㄥ叆妯″潡

鍔熻兘璇存槑锛?1. 鎻愪緵鏁版嵁搴撲細璇濅緷璧?2. 鎻愪緵褰撳墠鐢ㄦ埛渚濊禆
3. 鎻愪緵鏉冮檺鏍￠獙渚濊禆

浣跨敤绀轰緥锛?    from app.core.deps import get_db

    @router.get("/users")
    async def get_users(db: Session = Depends(get_db)):
        return db.query(User).all()
"""

from sqlalchemy.orm import Session
from typing import Generator
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

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
