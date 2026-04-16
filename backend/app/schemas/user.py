from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: str = None
    password: str = None

class UserResponse(UserBase):
    id: int

class UserDetailResponse(UserResponse):
    is_active: bool
    created_at: str  # Ideally, this should be a datetime
    updated_at: str

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str
