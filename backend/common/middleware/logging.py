"""鏃ュ織涓棿浠?""
from fastapi import Request
from loguru import logger
import time


async def logging_middleware(request: Request, call_next):
    """鏃ュ織涓棿浠?""
    start_time = time.time()
    
    # 璁板綍璇锋眰淇℃伅
    logger.info(f"璇锋眰: {request.method} {request.url.path}")
    
    # 澶勭悊璇锋眰
    response = await call_next(request)
    
    # 璁板綍鍝嶅簲淇℃伅
    process_time = time.time() - start_time
    logger.info(
        f"鍝嶅簲: {request.method} {request.url.path} "
        f"状态佺爜: {response.status_code} "
        f"鑰楁椂: {process_time:.3f}s"
    )
    
    return response
