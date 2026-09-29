from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.account import AccountResponse, AmountRequest, TransferRequest
from app.schemas.transaction import OperationResponse, TransactionResponse
from app.services.account_service import AccountService

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.get("/me", response_model=AccountResponse)
def get_my_account(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = AccountService(db).get_account(user)
    return AccountResponse(
        account_id=account.id,
        account_number=account.account_number,
        account_holder_name=user.name,
        balance=account.balance,
        created_at=account.created_at,
    )


@router.post("/deposit", response_model=OperationResponse)
def deposit(
    data: AmountRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account, tx = AccountService(db).deposit(user, data.amount)
    return OperationResponse(
        message="Deposit successful",
        balance=account.balance,
        transaction=TransactionResponse.model_validate(tx),
    )


@router.post("/withdraw", response_model=OperationResponse)
def withdraw(
    data: AmountRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account, tx = AccountService(db).withdraw(user, data.amount)
    return OperationResponse(
        message="Withdrawal successful",
        balance=account.balance,
        transaction=TransactionResponse.model_validate(tx),
    )


@router.post("/transfer", response_model=OperationResponse)
def transfer(
    data: TransferRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account, tx = AccountService(db).transfer(user, data.receiver_account_id, data.amount)
    return OperationResponse(
        message="Transfer successful",
        balance=account.balance,
        transaction=TransactionResponse.model_validate(tx),
    )


@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AccountService(db).history(user)
