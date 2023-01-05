from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class UserModel(BaseModel):
    first_name: str
    last_name: str
    login: str
    password: str
    date_of_birth: str

    class Config:
        orm_mode = True
