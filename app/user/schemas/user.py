from pydantic import BaseModel, Field
from app.image.schemas.image import ImageSchema
from core.fastapi.schemas import HashId
from core.fastapi.schemas.hashid import DehashId


class AccountAuthSchema(BaseModel):
    username: str = Field(..., description="Username")

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: HashId
    display_name: str
    is_admin: bool
    image: ImageSchema = None
    account_auth: AccountAuthSchema = None

    class Config:
        orm_mode = True


class UpdateUserSchema(BaseModel):
    id: DehashId
    display_name: str
    filename: str = None


class UpdateMeSchema(BaseModel):
    display_name: str
    filename: str = None


class CreateUserRequestSchema(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class CreateUserResponseSchema(BaseModel):
    username: str = Field(..., description="Username")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
