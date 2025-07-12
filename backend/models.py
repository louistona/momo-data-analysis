from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    sender = Column(String)
    receiver = Column(String)
    amount = Column(Integer)
    date = Column(DateTime)
    transaction_type = Column(String)