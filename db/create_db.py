from db_connection import Base, engine
from shared_models.Ledger import Ledger


Base.metadata.create_all(engine)