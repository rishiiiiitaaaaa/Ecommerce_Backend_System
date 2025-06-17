from fastapi import APIRouter, Depends, HTTPException, status #used for api routing , exception handling
from sqlalchemy.orm import Session #for db operations
from app.auth import schemas, models, utils
from app.core.database import get_db
from app.auth.jwt_handler import create_tokens #token creation
from app.utils.token_utils import generate_reset_token, verify_reset_token #for password reset token generation and verification
from app.utils.email_utils import send_reset_email
from app.auth.models import User 
from app.auth.schemas import ForgotPasswordRequest, ResetPasswordRequest
from app.core.logger import logger

# Define an APIRouter for all auth-related routes with a common prefix and tag
router = APIRouter(prefix="/auth", tags=["Auth"])
#for registration
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"Attempting signup for email: {user.email}")
    # Check if the user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        logger.warning(f"Signup failed: Email already registered - {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the password securely
    hashed_password = utils.hash_password(user.password)
    # Create new user instance
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    # Add and commit the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Refresh to get the ID and other DB-generated fields

    logger.info(f"User created successfully: {new_user.email} (ID: {new_user.id})")
    return {"message": "User created successfully"}

#for login 
@router.post("/signin")
def signin(user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.debug(f"Signin attempt for email: {user.email}")
     # Find user by email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()


    if not db_user:
        logger.warning(f"Signin failed: Invalid email - {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
    )

    if not utils.verify_password(plain_password=user.password, hashed_password=db_user.password):
        logger.warning(f"Signin failed: Incorrect password for {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
    )

    # Generate JWT token with user ID and role
    access_token = create_tokens({"sub": str(db_user.id), "role": db_user.role})
    logger.info(f"Signin successful for user: {user.email} (ID: {db_user.id})")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#for getting a mail to reset password
@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    logger.debug(f"Password reset requested for email: {data.email}")
     # search for user by email
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        logger.warning(f"Password reset failed: User not found - {data.email}")
        raise HTTPException(status_code=404, detail="User not found")
    # Generate secure token for password reset present in email
    token = generate_reset_token(user.email)
    # Send reset email
    send_reset_email(user.email, token)
    logger.info(f"Password reset email sent to: {user.email}")
    return {"message": "Reset link sent to your email"}

#resetting password using tokens
@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    logger.debug(f"Attempting password reset using token: {data.token}")
    # Validate the token and extract email
    email = verify_reset_token(data.token)
    # Find the user with the provided email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Password reset failed: User not found for email {email}")
        raise HTTPException(status_code=404, detail="User not found")
    # Update the user's password
    user.password = utils.hash_password(data.new_password)
    db.commit()
    logger.info(f"Password reset successful for user: {email}")
    return {"message": "Password has been reset successfully"}
