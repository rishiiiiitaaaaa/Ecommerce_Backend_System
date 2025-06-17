from fastapi import HTTPException, status, Request, Depends
from passlib.context import CryptContext #used to hash and verify passwords.
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.jwt_handler import decode_token
from app.auth import models  
from jose import JWTError
from app.core.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#Uses bcrypt for secure password hashing.
#deprecated="auto" ensures older algorithms can be updated transparently.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#This function gets the current authenticated user from the Authorization header.
# It’s typically used as a dependency in protected routes.
def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    #Get Authorization header
    auth_header = request.headers.get("Authorization")
    logger.debug(f"Authorization header received: {auth_header}")
    if not auth_header:
        logger.warning("Authorization header missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    #Validate Header Format
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        logger.warning("Invalid Authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )
    #Decode JWT
    try:
        logger.info("Decoding token")
        payload = decode_token(token)
        logger.debug(f"Token payload: {payload}")
    except JWTError as e:
        logger.error(f"Token decoding failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    #Extract and Validate Payload
    if payload is None:
        logger.warning("Token payload is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user_id = payload.get("sub")
    if not user_id:
        logger.warning("Token payload missing user ID")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload missing user ID")

    try:
        user_id = int(user_id)
    except ValueError:
        logger.warning("Invalid user ID in token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token")

    # Query the User
    logger.debug(f"Querying user with ID: {user_id}")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Return User Info
    logger.info(f"Authenticated user: {user.email} (ID: {user.id})")
    return {"id": user.id, "email": user.email, "role": user.role}