from sqlalchemy.orm import Session
import sys
import os
from db.shared_models.Ledger import Ledger
from sqlalchemy import func


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db.db_connection import SessionLocal

def get_all_ledger_entries(db: Session):
    return db.query(Ledger).all()


def get_ledger(owner_id: str) -> int:
    session = SessionLocal()
    try:
        # Calculate the sum of the 'amount' field for all ledger entries of the owner
        balance = session.query(func.sum(Ledger.amount)).filter(Ledger.owner_id == owner_id).scalar()
        # Return the balance or 0 if no entries are found
        return balance or 0
    finally:
        # Close the session
        session.close()