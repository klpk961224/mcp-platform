"""异常处理中间件"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger


async def exception_middleware(request: Request, call_next):
    """异常处理中间件"""
    try:
        return await call_next(request)
    except HTTPException as e:
        logger.error(f"HTTP异常: {e.status_code} - {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content={"code": e.status_code, "message": e.detail}
        )
    except Exception as e:
        logger.error(f"未捕获异常: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "message": "服务器内部错误"}
        )