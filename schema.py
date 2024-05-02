from pydantic import BaseModel, EmailStr, Field

class UserRegistration(BaseModel):
    username: str = Field('Username', min_length=4, max_length=20)
    email: EmailStr
    password: str = Field('Password', min_length=4)

class UserLogin(BaseModel):
    email: EmailStr
    password_hash: str = Field('Password', min_length=4)
