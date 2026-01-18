"""
认证域服务?- FastAPI搴旂敤鍏ュ彛

鍔熻兘璇存槑锛?1. 创建FastAPI搴旂敤
2. 閰嶇疆涓棿浠?3. 娉ㄥ唽璺敱
4. 鍚姩鏈嶅姟

浣跨敤绀轰緥锛?    uvicorn app.main:app --host 0.0.0.0 --port 28001 --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
import os

# 娣诲姞椤圭洰鏍圭洰褰曞埌Python璺緞
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app.core.config import settings
from app.api.v1 import auth
from common.database.connection import datasource_manager

# 创建FastAPI搴旂敤
app = FastAPI(
    title=settings.APP_NAME,
    description="认证域服务?- JWT璁よ瘉銆乀oken绠＄悊",
    version="1.0.0",
    debug=settings.APP_DEBUG
)

# 閰嶇疆CORS涓棿浠?app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 鐢熶骇鐜搴旇璁剧疆鍏蜂綋鐨勫煙鍚?    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 娉ㄥ唽璺敱
app.include_router(auth.router, prefix="/api/v1")


@app.get("/", summary="鍋ュ悍妫€鏌?)
async def root():
    """
    鍋ュ悍妫€鏌ユ帴鍙?    
    Returns:
        dict: 鏈嶅姟状态佷俊鎭?    
    浣跨敤绀轰緥锛?        GET /
    """
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", summary="鍋ュ悍妫€鏌?)
async def health():
    """
    鍋ュ悍妫€鏌ユ帴鍙?    
    Returns:
        dict: 鏈嶅姟鍋ュ悍状态?    
    浣跨敤绀轰緥锛?        GET /health
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


@app.on_event("startup")
async def startup_event():
    """搴旂敤鍚姩浜嬩欢"""
    logger.info(f"{settings.APP_NAME} 鍚姩涓?..")
    logger.info(f"鐜: {settings.APP_ENV}")
    logger.info(f"绔彛: {settings.APP_PORT}")
    
    # 娉ㄥ唽鏁版嵁婧?    try:
        # 瑙ｆ瀽 DATABASE_URL
        db_url = settings.DATABASE_URL
        if db_url.startswith("mysql+pymysql://"):
            # 鏍煎紡: mysql+pymysql://username:password@host:port/database
            url_without_prefix = db_url.replace("mysql+pymysql://", "")
            auth_part, host_port_db = url_without_prefix.split("@")
            username, password = auth_part.split(":")
            host_port, database = host_port_db.split("/")
            host, port = host_port.split(":")
            
            datasource_manager.register_datasource(
                name='mysql',
                db_type='mysql',
                host=host,
                port=int(port),
                username=username,
                password=password,
                database=database,
                pool_size=10,
                max_overflow=20,
                echo=False
            )
            logger.info(f"鏁版嵁婧愭敞鍐屾垚鍔? mysql -> {host}:{port}/{database}")
    except Exception as e:
        logger.error(f"鏁版嵁婧愭敞鍐屽け璐? {e}")
        raise
    
    logger.info(f"{settings.APP_NAME} 鍚姩瀹屾垚")


@app.on_event("shutdown")
async def shutdown_event():
    """搴旂敤鍏抽棴浜嬩欢"""
    logger.info(f"{settings.APP_NAME} 鍏抽棴涓?..")


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"鍚姩 {settings.APP_NAME}...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
