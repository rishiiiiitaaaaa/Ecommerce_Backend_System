import os
from itsdangerous import URLSafeTimedSerializer #This is a secure way to encode data into time-sensitive tokens that can be safely used in URLs
from fastapi import HTTPException

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-if-not-set") 
# Loads the SECRET_KEY from environment variables (usually set in a .env file).If it isn't found, it uses a fallback string for local/testing purposes.This key is crucial for signing and verifying tokens securely."""
serializer = URLSafeTimedSerializer(SECRET_KEY) #Creates a serializer object using the SECRET_KEY.This object can now generate (dumps) and validate (loads) secure tokens.

#Token Generation
def generate_reset_token(email: str) -> str: #Takes an email address and returns a time-safe token.
    return serializer.dumps(email, salt="password-reset")

def verify_reset_token(token: str, expiration=3600): #Takes a token and checks if it's valid and not expired.
    try:
        email = serializer.loads(token, salt="password-reset", max_age=expiration)
        return email
    except Exception:#If decoding fails an HTTP 400 error is raised 
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
#the salt="password-reset" is a namespace or category label used to add extra protection when generating and verifying tokens.
#A salt ensures that tokens for one purpose cannot be confused with or reused for another purpose — even if the same data is encoded.