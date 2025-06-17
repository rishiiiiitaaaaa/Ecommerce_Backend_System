from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from app.core.logger import logger  

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# Accepts user data to encode into the token.
def create_tokens(data: dict, expires_delta: timedelta = None):
    logger.debug(f"Creating token for data: {data}")
    
    to_encode = data.copy()
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        logger.debug(f"'sub' claim converted to string: {to_encode['sub']}")
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token created successfully for sub: {to_encode.get('sub')}")
    
    return token

# Accepts a JWT string and attempts to decode it.
def decode_token(token: str):
    logger.debug("Attempting to decode JWT token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" in payload and not isinstance(payload["sub"], str):
            logger.debug("Converted 'sub' claim to string")
            payload["sub"] = str(payload["sub"])
        logger.info(f"Token decoded successfully for sub: {payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.error(f"[JWTError] Failed to decode token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


# FastAPI dependency to extract and decode the token from the request.
def get_current_user(request: Request):
    logger.debug("Extracting Authorization header from request")
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        logger.warning("Authorization header missing")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    try:
        scheme, token = auth_header.split(" ")
    except ValueError:
        logger.warning("Authorization header format is invalid")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")

    if scheme.lower() != "bearer" or not token:
        logger.warning("Authorization scheme is not Bearer or token is missing")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")

    logger.debug("Authorization header successfully parsed, decoding token...")
    return decode_token(token)


# Validates user and checks for admin role.
def get_current_admin_user(request: Request):
    logger.debug("Checking if current user has admin privileges")
    user = get_current_user(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    
    logger.info(f"Admin access granted for user: {user.get('sub')}")
    return user
def get_current_user_only(request: Request):
    logger.debug("Checking if its a user")
    user = get_current_user(request)
    if user.get("role") != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user privileges required")
    user["id"] = user.get("id") or user.get("sub")
    return user
   
