"""
权限域服务?- FastAPI搴旂敤鍏ュ彛
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app.core.config import settings
from app.api.v1 import roles, permissions, menus, data_scopes
from common.database.connection import datasource_manager

app = FastAPI(
    title=settings.APP_NAME,
    description="权限域服务?- 瑙掕壊绠＄悊銆佹潈闄愮鐞嗐€佽彍鍗曠鐞嗐€佹暟鎹寖鍥存潈闄?,
    version="1.0.0",
    debug=settings.APP_DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roles.router, prefix="/api/v1")
app.include_router(permissions.router, prefix="/api/v1")
app.include_router(menus.router, prefix="/api/v1")
app.include_router(data_scopes.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


@app.on_event("startup")
async def startup_event():
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
