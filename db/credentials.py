#Class because additional properties can be defined
class Credentials:
    _DATABASE_URL = "postgresql://postgres:Uygr12_!@localhost/monorepo_ledger_db"

    #read only
    @property
    def DATABASE_URL(self) -> str:
       return self._DATABASE_URL
    
CREDENTIALS = Credentials()