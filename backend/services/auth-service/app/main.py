"""
认证域服务 - FastAPI应用入口

功能说明：
1. 创建FastAPI应用
2. 配置中间件
3. 注册路由
4. 启动服务

使用示例：
    uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings
from app.api.v1 import auth
from common.database.connection import datasource_manager

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="认证域服务 - JWT认证、Token管理",
    version="1.0.0",
    debug=settings.APP_DEBUG
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")


@app.get("/", summary="健康检查")
async def root():
    """
    健康检查接口
    
    Returns:
        dict: 服务状态信息
    
    使用示例：
        GET /
    """
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", summary="健康检查")
async def health():
    """
    健康检查接口
    
    Returns:
        dict: 服务健康状态
    
    使用示例：
        GET /health
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
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
    """应用关闭事件"""
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