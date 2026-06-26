from pydantic import BaseModel

class AccountBase(BaseModel):
    name: str
    balance: float

class AccountCreate(AccountBase):
    user_id: int

class AccountUpdate(BaseModel):
    name: str | None = None
    balance: float | None = None

class AccountResponse(AccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True