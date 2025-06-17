from pydantic import BaseModel, field_validator #A decorator to add custom field-level validation 
import re #used for email format checking.

# Defines a set of allowed top-level domains (TLDs)
VALID_TLDS = {
    "com", "gov", "co", "in"
}
#for user registration
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(\w{2,})$"
        match = re.match(email_regex, v)
        if not match:
            raise ValueError("Invalid email format")
        
        tld = match.group(1).lower()
        if tld not in VALID_TLDS:
            raise ValueError(f"Invalid or unsupported email domain (TLD: .{tld})")
        
        return v.lower()
#for user login
class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(\w{2,})$"
        match = re.match(email_regex, v)
        if not match:
            raise ValueError("Invalid email format")
        
        tld = match.group(1).lower()
        if tld not in VALID_TLDS:
            raise ValueError(f"Invalid or unsupported email domain (TLD: .{tld})")
        
        return v.lower()
#To return user details
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str 

model_config = {
        "from_attributes": True
    }
#To initiate password reset
class ForgotPasswordRequest(BaseModel):
    email: str
#To reset password using tokens
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str