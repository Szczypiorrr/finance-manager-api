from pydantic import BaseModel

class AccountBase(BaseModel):
    """Base schema for account data."""

    name: str

class AccountCreate(AccountBase):
    """Schema for creating an account."""

    user_id: int

class AccountUpdate(AccountBase):
    """Schema for updating an account."""

    pass

class AccountDeposit(BaseModel):
    """Schema for depositing money into an account."""

    amount: float

class AccountWithdraw(BaseModel):
    """Schema for withdrawing money from an account."""

    amount: float

class AccountTransfer(BaseModel):
    """Schema for transferring money between accounts."""

    sender_id: int
    receiver_id: int
    amount: float

class AccountResponse(AccountBase):
    """Schema returned for account data."""

    balance: float
    id: int
    user_id: int

    class Config:
        from_attributes = True

class AccountTransferResponse(BaseModel):
    """Schema returned after a successful transfer."""

    amount: float
    sender_id: int
    sender_balance: float
    receiver_id: int
    receiver_balance: float

    class Config:
        from_attributes = True