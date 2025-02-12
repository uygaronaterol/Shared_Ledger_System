from core.base_ledger_operation import BaseLedgerOperation
from enum import Enum

class AdditionalOperations(str, Enum):
    WITHDRAW_CREDIT = "WITHDRAW_CREDIT"

# Combine enums
combined_members = {**BaseLedgerOperation.__members__, **AdditionalOperations.__members__}
BankOperation = Enum('BankOperation', combined_members)





