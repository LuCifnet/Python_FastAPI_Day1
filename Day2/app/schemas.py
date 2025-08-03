import re
from pydantic import BaseModel, EmailStr, field_validator

ALLOWED_DOMAINS = {"@gmail.com", "@yahoo.com", "@outlook.com"}
def get_domain(email: str) -> str:
    return "@" + email.split("@")[-1]

#data models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    model_config = {"extra": "forbid"}

    @field_validator("email", mode="before")
    @classmethod
    def preprocess_email(cls, value: str) -> str:
        return value.replace(" ", "").lower()

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: str) -> str:
        domain = get_domain(value)
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Email domain '{domain}' is not allowed. Allowed domains: {ALLOWED_DOMAINS}")
        return value

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        rules = [
            (r'.{8,}', "Password must be at least 8 characters long"),
            (r'[A-Z]', "Password must contain at least one uppercase letter"),
            (r'[a-z]', "Password must contain at least one lowercase letter"),
            (r'\d', "Password must contain at least one digit"),
            (r'[!@#$%^&*(),.?\":{}|<>]', "Password must contain at least one special character"),
        ]
        for pattern, error_msg in rules:
            if not re.search(pattern, value):
                raise ValueError(error_msg)
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str