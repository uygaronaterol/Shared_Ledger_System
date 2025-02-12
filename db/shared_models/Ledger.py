from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from core.base_ledger_operation import BaseLedgerOperation
from db.db_connection import Base


#Database table class 
class Ledger(Base):
    __tablename__ = "ledger"  

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(SQLAlchemyEnum(BaseLedgerOperation), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, unique=True, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Ledger(id={self.id}, operation={self.operation}, amount={self.amount}, owner_id={self.owner_id})>"
