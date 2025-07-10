from fastapi.responses import JSONResponse
from typing import Optional, Any

def format_response(
    success: bool,
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> JSONResponse:
    """
    Base response formatter.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "message": message,
            "data": data or {}
        }
    )

def success_response(
    message: str,
    data: Optional[Any] = None
) -> JSONResponse:
    """
    Standard 200 OK success response.
    """
    return format_response(True, message, data, status_code=200)

def error_response(
    message: str,
    data: Optional[Any] = None,
    status_code: int = 400
) -> JSONResponse:
    """
    Standard error response (default 400 Bad Request).
    """
    return format_response(False, message, data, status_code=status_code)
