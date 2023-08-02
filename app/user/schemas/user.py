from pydantic import BaseModel, Field
from core.fastapi.schemas.hashid import HashId


class UserSchema(BaseModel):
    id: HashId
    display_name: str
    username: str
    is_admin: bool

    class Config:
        orm_mode = True


class UpdateUserSchema(BaseModel):
    display_name: str
    username: str
    password: str = None


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


class SetAdminSchema(BaseModel):
    is_admin: bool
