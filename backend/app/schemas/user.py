from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str