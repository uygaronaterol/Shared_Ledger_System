from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
import sys
import os
from pydantic import BaseModel, condecimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from bank_app.models.models import BankOperation
from bank_app.db import db
router = APIRouter()

#pydantic model
class LedgerTransaction(BaseModel): #serializer
    owner_id: str
    ledger_operation: BankOperation 
    amount: int
    nonce: str

#HTTP methods
@router.get('/')
def index():
    return {"test": "Hello World"}

@router.get('/ledger')
def index():
    return {"test": "Hello World"}

@router.get("/ledger/{owner_id}", response_model=int)
def get_ledger(owner_id:str):
    return db.get_ledger(owner_id)

@router.post("/ledger", status_code=status.HTTP_201_CREATED)
def ledger_transaction(transaction: LedgerTransaction):
    return db.process_ledger_transaction(transaction)