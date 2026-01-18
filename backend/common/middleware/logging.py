"""日志中间件"""
from fastapi import Request
from loguru import logger
import time


async def logging_middleware(request: Request, call_next):
    """日志中间件"""
    start_time = time.time()
    
    # 记录请求信息
    logger.info(f"请求: {request.method} {request.url.path}")
    
    # 处理请求
    response = await call_next(request)
    
    # 记录响应信息
    process_time = time.time() - start_time
    logger.info(
        f"响应: {request.method} {request.url.path} "
        f"状态码: {response.status_code} "
        f"耗时: {process_time:.3f}s"
    )
    
    return response