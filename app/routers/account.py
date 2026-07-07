from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.account import AccountResponse, AccountCreate, AccountUpdate, AccountDeposit, AccountWithdraw, AccountTransfer, AccountTransferResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.account as account_service
from app.exceptions.account_exceptions import AccountNotFound, AccountAlreadyExists
from app.exceptions.user_exceptions import UserNotFound
from app.exceptions.common_exceptions import InvalidAmount
from app.exceptions.account_exceptions import InvalidTransfer, InsufficientFunds


router = APIRouter(tags=["Accounts"], prefix="/accounts")

@router.get("/", response_model=list[AccountResponse])
def read_accounts(limit: int = 10, offset: int = 0, user_id: int = None, db: Session = Depends(get_db)):
    """Return a list of accounts."""

    return account_service.get_accounts(db=db, user_id=user_id, limit=limit, offset=offset)

@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    """Return an account by its ID."""

    try:
        return account_service.get_account_by_id(account_id=account_id, db=db)
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """Create a new account."""

    try:
        return account_service.create_account(account=account, db=db)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID not found")
    except AccountAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account with this name already exists")

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """Delete an account."""

    try:
        return account_service.delete_account(account_id=account_id, db=db)
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, account_update: AccountUpdate, db: Session = Depends(get_db)):
    """Update an existing account."""

    try:
        return account_service.update_account(account_id=account_id, account_update=account_update, db=db)
    except AccountAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account with this name already exists")
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

@router.post("/{account_id}/deposit", response_model=AccountResponse)
def deposit_to_account(account_id: int, deposit: AccountDeposit, db: Session = Depends(get_db)):
    """Deposit money into an account."""

    try:
        return account_service.deposit_to_account(account_id=account_id, amount=deposit.amount, db=db)
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")
    
@router.post("/{account_id}/withdraw", response_model=AccountResponse)
def withdraw_from_account(account_id: int, withdraw: AccountWithdraw, db: Session = Depends(get_db)):
    """Withdraw money from an account."""

    try:
        return account_service.withdraw_from_account(account_id=account_id, amount=withdraw.amount, db=db)
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")
    except InsufficientFunds:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
    
@router.post("/transfer", response_model=AccountTransferResponse)
def transfer_between_accounts(transfer: AccountTransfer, db: Session = Depends(get_db)):
    """Transfer money between two accounts."""

    try:
        return account_service.transfer_between_accounts(sender_id=transfer.sender_id, receiver_id=transfer.receiver_id, amount=transfer.amount, db=db)
    except InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except InvalidTransfer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot transfer to the same account")
    except InsufficientFunds:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")