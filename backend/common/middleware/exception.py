"""寮傚父澶勭悊涓棿浠?""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger


async def exception_middleware(request: Request, call_next):
    """寮傚父澶勭悊涓棿浠?""
    try:
        return await call_next(request)
    except HTTPException as e:
        logger.error(f"HTTP寮傚父: {e.status_code} - {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content={"code": e.status_code, "message": e.detail}
        )
    except Exception as e:
        logger.error(f"鏈崟鑾峰紓甯? {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "message": "鏈嶅姟鍣ㄥ唴閮ㄩ敊璇?}
        )
