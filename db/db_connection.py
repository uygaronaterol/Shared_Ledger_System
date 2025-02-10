from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.credentials import CREDENTIALS


engine=create_engine(CREDENTIALS.DATABASE_URL, echo=True)

SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()