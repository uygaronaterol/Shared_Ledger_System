from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import sys
import os
from sqlalchemy import func
from fastapi import HTTPException, status
from pydantic import BaseModel, condecimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db.db_connection import SessionLocal
from db.shared_models.Ledger import Ledger
from bank_app.models.models import BankOperation

#pydantic model
class LedgerTransaction(BaseModel): #serializer
    owner_id: str
    ledger_operation: BankOperation
    amount: int
    nonce: str


def get_all_ledger_entries(db: Session):
    return db.query(Ledger).all()


def get_ledger(owner_id: str) -> int:
    session = SessionLocal()
    try:
        # calculate the sum of all ledgers with owner id
        balance = session.query(func.sum(Ledger.amount)).filter(Ledger.owner_id == owner_id).scalar()
        return balance or 0
    finally:
        # close the local session
        session.close()

def process_ledger_transaction( transaction: LedgerTransaction):

    session = SessionLocal()
    new_entry = 0
    try:
        match transaction.ledger_operation:
            case BankOperation.DAILY_REWARD:

                # the logic i found is every day only one time this method is executed I assume signup credit comes before daily credit 
                # (so there must be an entry with this nonce)
                # I thought the amount in body is for these puposes not the configuration and added the amount for now
                existing_entry = session.query(Ledger).filter(Ledger.nonce == transaction.nonce and Ledger.owner_id == transaction.owner_id).first()
                if not existing_entry:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Daily reward only applicable to already existed ledgers."
                    )
                
                # is daily reward already claimed ?
                today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                today_end = today_start + timedelta(days=1)

                reward_claimed = session.query(Ledger).filter(
                    Ledger.owner_id == transaction.owner_id,
                    Ledger.nonce == transaction.nonce,
                    Ledger.operation == "DAILY_REWARD",
                    Ledger.created_on >= today_start,
                    Ledger.created_on < today_end
                ).first()

                if reward_claimed:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Daily reward has already been claimed today."
                    )

                # Create new ledger operation entry for daily reward
                new_entry = Ledger(
                    owner_id=transaction.owner_id,
                    operation="DAILY_REWARD",
                    amount=transaction.amount,
                    nonce=transaction.nonce
                )

                #Add legder operation commit and we are done
                session.add(new_entry)
                session.commit()
                session.refresh(new_entry)
                session.close()
                return new_entry
            case BankOperation.SIGNUP_CREDIT:
                
                #If not got the credit give the credit and we are done Did not check already existed nonce cause i assume no operations made before this
                reward_claimed = session.query(Ledger).filter(
                    Ledger.nonce == transaction.nonce,
                    Ledger.owner_id == transaction.owner_id,
                    Ledger.operation == "SIGNUP_CREDIT",
                ).first()

                if reward_claimed:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Sign up credit has already been creates."
                    )

                # Give signup reward
                new_entry = Ledger(
                    owner_id=transaction.owner_id,
                    operation="SIGNUP_CREDIT",
                    amount=transaction.amount,
                    nonce=transaction.nonce
                )

                #Add legder operation commit and we are done
                session.add(new_entry)
                session.commit()
                session.refresh(new_entry)
                session.close()
                return new_entry

            case BankOperation.CREDIT_SPEND:
                
                # We do not need to check if ledger exists cause we already check it by just checking the balance
                current_balance = session.query(func.sum(Ledger.amount)).filter(Ledger.nonce == LedgerTransaction.nonce and Ledger.owner_id == transaction.owner_id).scalar()

                # Validate sufficient balance
                if current_balance < transaction.amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Insufficient balance."
                    )
                
                # Take credit spent (I assume the amount they enter is negative)
                new_entry = Ledger(
                    owner_id=transaction.owner_id,
                    operation="CREDIT_SPEND",
                    amount=-abs(transaction.amount),
                    nonce=transaction.nonce
                )

                #Add legder operation commit and we are done
                session.add(new_entry)
                session.commit()
                session.refresh(new_entry)
                session.close()
                return new_entry

            case BankOperation.CREDIT_ADD:

                # I am assuming sign up credit added first so I check if the ledger exists first by this code
                existing_entry = session.query(Ledger).filter(Ledger.nonce == transaction.nonce and Ledger.owner_id == transaction.owner_id).first()
                if not existing_entry:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Credit can only be added to already existed ledgers."
                    )
                
                # Add credit
                new_entry = Ledger(
                    owner_id=transaction.owner_id,
                    operation="CREDIT_ADD",
                    amount=transaction.amount,
                    nonce=transaction.nonce
                )

                #Add legder operation commit and we are done
                session.add(new_entry)
                session.commit()
                session.refresh(new_entry)
                session.close()
                return new_entry

            case BankOperation.WITHDRAW_CREDIT:
                # Same as credit spent
                current_balance = session.query(func.sum(Ledger.amount)).filter(Ledger.nonce == LedgerTransaction.nonce and Ledger.owner_id == transaction.owner_id).scalar()

                # Validate sufficient balance
                if current_balance < transaction.amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Insufficient balance."
                    )
                
                # Take credit spent (I assume the amount they enter is negative)
                new_entry = Ledger(
                    owner_id=transaction.owner_id,
                    operation=transaction.ledger_operation,
                    amount=-abs(transaction.amount),
                    nonce=transaction.nonce
                )

                #Add legder operation commit and we are done
                session.add(new_entry)
                session.commit()
                session.refresh(new_entry)
                session.close()
                return new_entry
            
            case _:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid ledger operation."
                )
                

    finally:
        session.close()

    