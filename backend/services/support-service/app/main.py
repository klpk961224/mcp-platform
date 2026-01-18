# -*- coding: utf-8 -*-
"""
鏀拺鏈嶅姟涓诲簲鐢?
鍔熻兘璇存槑锛?1. 寰呭姙浠诲姟绠＄悊
2. 鏃ュ織绠＄悊
3. 閫氱煡绠＄悊

浣跨敤绀轰緥锛?    from app.main import app
    
    # 鍚姩鏈嶅姟
    uvicorn app.main:app --host 0.0.0.0 --port 28005
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from loguru import logger
import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app.core.config import settings
from common.database.connection import datasource_manager
from app.api.v1 import router as v1_router


# 鍒涘缓FastAPI搴旂敤
app = FastAPI(
    title="鏀拺鏈嶅姟API",
    description="浼佷笟绾I缁煎悎绠＄悊骞冲彴 - 鏀拺鏈嶅姟",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# 閰嶇疆CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 鐢熶骇鐜搴旇閰嶇疆鍏蜂綋鐨勫煙鍚?    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 娉ㄥ唽璺敱
app.include_router(v1_router)


# 鑷畾涔塐penAPI閰嶇疆
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="鏀拺鏈嶅姟API",
        version="1.0.0",
        description="浼佷笟绾I缁煎悎绠＄悊骞冲彴 - 鏀拺鏈嶅姟",
        routes=app.routes,
    )
    
    # 娣诲姞API鐗堟湰淇℃伅
    openapi_schema["info"]["x-api-version"] = "1.0.0"
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# 鍋ュ悍妫€鏌ョ鐐?@app.get("/health", tags=["鍋ュ悍妫€鏌?])
async def health_check():
    """鍋ュ悍妫€鏌ョ鐐?""
    return {
        "status": "healthy",
        "service": "support-service",
        "version": "1.0.0"
    }


# 鍏ㄥ眬寮傚父澶勭悊
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """鍏ㄥ眬寮傚父澶勭悊鍣?""
    logger.error(f"鍏ㄥ眬寮傚父: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "鍐呴儴鏈嶅姟鍣ㄩ敊璇?,
            "message": str(exc)
        }
    )


# 鍚姩浜嬩欢
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


# 鍏抽棴浜嬩欢
@app.on_event("shutdown")
async def shutdown_event():
    """搴旂敤鍏抽棴浜嬩欢"""
    logger.info("鏀拺鏈嶅姟鍏抽棴")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.APP_ENV == "development"
    )
