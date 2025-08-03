from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import traceback
from fastapi.responses import JSONResponse


async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response Status: {response.status_code}")
    return response


async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print("Error: ", traceback.format_exc())
        return JSONResponse(
            status_code= 500, content={"detail": "Something went wrong. Please try again later."}
        )