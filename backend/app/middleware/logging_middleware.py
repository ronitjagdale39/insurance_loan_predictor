import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.core.logging_config import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status={response.status_code} | "
            f"Time={process_time:.2f} ms"
        )

        return response
        