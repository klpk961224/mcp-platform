"""
权限域服务 - FastAPI应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings
from app.api.v1 import roles, permissions, menus
from common.database.connection import datasource_manager

app = FastAPI(
    title=settings.APP_NAME,
    description="权限域服务 - 角色管理、权限管理、菜单管理",
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
    logger.info(f"{settings.APP_NAME} 启动中...")
    logger.info(f"环境: {settings.APP_ENV}")
    logger.info(f"端口: {settings.APP_PORT}")
    
    # 注册数据源
    try:
        # 解析 DATABASE_URL
        db_url = settings.DATABASE_URL
        if db_url.startswith("mysql+pymysql://"):
            # 格式: mysql+pymysql://username:password@host:port/database
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
            logger.info(f"数据源注册成功: mysql -> {host}:{port}/{database}")
    except Exception as e:
        logger.error(f"数据源注册失败: {e}")
        raise
    
    logger.info(f"{settings.APP_NAME} 启动完成")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{settings.APP_NAME} 关闭中...")


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"启动 {settings.APP_NAME}...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )