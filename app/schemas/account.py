from pydantic import BaseModel

class AccountBase(BaseModel):
    name: str

class AccountCreate(AccountBase):
    user_id: int

class AccountUpdate(AccountBase):
    pass

class AccountDeposit(BaseModel):
    amount: float

class AccountWithdraw(BaseModel):
    amount: float

class AccountTransfer(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

class AccountResponse(AccountBase):
    balance: float
    id: int
    user_id: int

    class Config:
        from_attributes = True

class AccountTransferResponse(BaseModel):
    amount: float
    sender_id: int
    sender_balance: float
    receiver_id: int
    receiver_balance: float

    class Config:
        from_attributes = True