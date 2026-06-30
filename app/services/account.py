from models.account import Account
from schemas.account import AccountUpdate
from sqlalchemy.orm import Session
from services.user import get_user_by_id

class AccountNotFound(Exception):
    pass

class AccountAlreadyExists(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class InvalidAmount(Exception):
    pass

class InvalidTransfer(Exception):
    pass

def get_accounts(db: Session, user_id: int = None, limit: int = 10, offset: int = 0):
    query = db.query(Account)
    if user_id is not None:
        query = query.where(Account.user_id == user_id)

    return query.limit(limit).offset(offset).all()

def get_account_by_id(account_id: int, db: Session):
    account = db.query(Account).where(Account.id == account_id).first()

    if not account:
        raise AccountNotFound()
    
    return account

def get_account_by_name(account_name: str, db: Session):
    return db.query(Account).where(Account.name == account_name).first()

def create_account(account: Account, db: Session):
    if get_account_by_name(account_name=account.name, db=db):
        raise AccountAlreadyExists()

    get_user_by_id(user_id=account.user_id, db=db)

    account_db = Account(name=account.name, balance=0, user_id=account.user_id)

    db.add(account_db)
    db.commit()
    db.refresh(account_db)

    return account_db

def delete_account(account_id: int, db: Session):
    account = get_account_by_id(account_id=account_id, db=db)

    db.delete(account)
    db.commit()

    return

def update_account(account_id: int, account_update: AccountUpdate, db: Session):
    account = get_account_by_id(account_id=account_id, db=db)

    if account_update.name == account.name:
        return account

    if get_account_by_name(account_name=account_update.name, db=db):
        raise AccountAlreadyExists()

    if account_update.name:
        account.name = account_update.name

    db.commit()
    db.refresh(account)

    return account

def deposit_to_account(account_id: int, amount: float, db: Session):
    account = get_account_by_id(account_id=account_id, db=db)

    if amount <= 0:
        raise InvalidAmount()

    account.balance += amount

    db.commit()
    db.refresh(account)

    return account

def withdraw_from_account(account_id: int, amount: float, db: Session):
    account = get_account_by_id(account_id=account_id, db=db)

    if amount <= 0:
        raise InvalidAmount()

    if account.balance < amount:
        raise InsufficientFunds()

    account.balance -= amount

    db.commit()
    db.refresh(account)

    return account

def transfer_between_accounts(sender_id: int, receiver_id: int, amount: float, db: Session):
    if amount <= 0:
        raise InvalidAmount()

    sender_account = get_account_by_id(account_id=sender_id, db=db)
    receiver_account = get_account_by_id(account_id=receiver_id, db=db)

    if sender_account.id == receiver_account.id:
        raise InvalidTransfer()

    if sender_account.balance < amount:
        raise InsufficientFunds()

    sender_account.balance -= amount
    receiver_account.balance += amount

    db.commit()
    db.refresh(sender_account)
    db.refresh(receiver_account)

    return {
        "amount": amount,
        "sender_id": sender_account.id,
        "sender_balance": sender_account.balance,
        "receiver_id": receiver_account.id,
        "receiver_balance": receiver_account.balance
    }