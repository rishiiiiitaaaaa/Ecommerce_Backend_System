from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

#Defines a function to handle exceptions of type HTTPException
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, #exc: the actual HTTPException that was raised.
        content={
            "error": True,
            "message": exc.detail,
            "code": exc.status_code
        }
    )

#Defines a function to catch any exception that is not an HTTPException
def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "code": HTTP_500_INTERNAL_SERVER_ERROR
        }
    )
