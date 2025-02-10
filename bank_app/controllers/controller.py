from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bank_app.db import db
from core.base_ledger_operation import BaseLedgerOperation

router = APIRouter()

#HTTP methods
@router.get('/')
def index():
    return {"test": "Hello World"}

@router.get('/ledger')
def index():
    return {"test": "Hello World"}

# @router.get('/ledger')
# def get_ledger_entries(db: Session = Depends(get_db)):
#     # Call function to get all ledger entries
#     ledger_entries = db.get_all_ledger_entries(db)
#     return {"ledger_entries": ledger_entries} 


class LedgerOperationRequest(BaseModel):
    operation: BaseLedgerOperation
    amount: int
    nonce: str
    owner_id: str


@router.get("/ledger/{owner_id}", response_model=int)
def get_ledger(owner_id:str):
    return db.get_ledger(owner_id)