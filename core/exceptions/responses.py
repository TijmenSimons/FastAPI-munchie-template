from pydantic import BaseModel


class ExceptionResponseSchema(BaseModel):
    error_code: str
    message: str
