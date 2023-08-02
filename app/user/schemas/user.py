from pydantic import BaseModel, Field
from core.fastapi.schemas import HashId
from core.fastapi.schemas.hashid import DehashId


class UserSchema(BaseModel):
    id: HashId
    display_name: str
    username: str
    is_admin: bool

    class Config:
        orm_mode = True


class UpdateUserSchema(BaseModel):
    id: DehashId
    display_name: str
    username: str
    password: str


class UpdateMeSchema(BaseModel):
    display_name: str
    username: str
    password: str


class CreateUserSchema(BaseModel):
    display_name: str
    username: str
    password: str


class CreateUserResponseSchema(BaseModel):
    username: str = Field(..., description="Username")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
