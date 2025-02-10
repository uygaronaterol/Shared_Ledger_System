from core.base_ledger_operation import BaseLedgerOperation

class WithdrawalOperation(BaseLedgerOperation):

    DAILY_REWARD = BaseLedgerOperation.DAILY_REWARD
    SIGNUP_CREDIT = BaseLedgerOperation.SIGNUP_CREDIT
    CREDIT_SPEND = BaseLedgerOperation.CREDIT_SPEND
    CREDIT_ADD = BaseLedgerOperation.CREDIT_ADD
    
    # Specific
    WITHDRAW_CREDIT = 0

class AddOperation(BaseLedgerOperation):

    DAILY_REWARD = BaseLedgerOperation.DAILY_REWARD
    SIGNUP_CREDIT = BaseLedgerOperation.SIGNUP_CREDIT
    CREDIT_SPEND = BaseLedgerOperation.CREDIT_SPEND
    CREDIT_ADD = BaseLedgerOperation.CREDIT_ADD
    
    # Specific
    ADDCREDIT = 0