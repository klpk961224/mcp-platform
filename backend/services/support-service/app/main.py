# -*- coding: utf-8 -*-
"""
支撑服务主应用

功能说明：
1. 待办任务管理
2. 日志管理
3. 通知管理

使用示例：
    from app.main import app
    
    # 启动服务
    uvicorn app.main:app --host 0.0.0.0 --port 8005
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from loguru import logger
import uvicorn

from common.config.settings import settings
from common.database.connection import datasource_manager
from app.api.v1 import router as v1_router


# 创建FastAPI应用
app = FastAPI(
    title="支撑服务API",
    description="企业级AI综合管理平台 - 支撑服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(v1_router)


# 自定义OpenAPI配置
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="支撑服务API",
        version="1.0.0",
        description="企业级AI综合管理平台 - 支撑服务",
        routes=app.routes,
    )
    
    # 添加API版本信息
    openapi_schema["info"]["x-api-version"] = "1.0.0"
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# 健康检查端点
@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "support-service",
        "version": "1.0.0"
    }


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"全局异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "内部服务器错误",
            "message": str(exc)
        }
    )


# 启动事件
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


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("支撑服务关闭")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8005,
        reload=settings.APP_ENV == "development"
    )