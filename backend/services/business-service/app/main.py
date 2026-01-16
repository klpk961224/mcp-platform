# -*- coding: utf-8 -*-
"""
业务服务主应用

功能说明：
1. 工作流管理
2. 审批流程
3. 业务逻辑

使用示例：
    from app.main import app
    
    # 启动服务
    uvicorn app.main:app --host 0.0.0.0 --port 8006
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from loguru import logger
import uvicorn

from common.config.settings import settings
from app.api.v1 import router as v1_router


# 创建FastAPI应用
app = FastAPI(
    title="业务服务API",
    description="企业级AI综合管理平台 - 业务服务",
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
        title="业务服务API",
        version="1.0.0",
        description="企业级AI综合管理平台 - 业务服务",
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
        "service": "business-service",
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
    logger.info("业务服务启动")


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("业务服务关闭")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8006,
        reload=settings.APP_ENV == "development"
    )