from fastapi import Request
from fastapi.responses import JSONResponse


async def internal_server_error(request: Request, exc: Exception):
    return JSONResponse({"detail": "Unexpected error occurred"}, status_code=500)