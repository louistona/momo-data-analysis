from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Transaction
from config import Config
from parse_xml import parse_sms_xml
import logging

def load_transactions(xml_file):
    logging.basicConfig(
        filename=Config.LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    transactions = parse_sms_xml(xml_file)
    try:
        for t in transactions:
            exists = session.query(Transaction).filter_by(
                message=t['message'],
                date=t['date']
            ).first()
            if not exists:
                transaction = Transaction(
                    message=t['message'],
                    sender=t['sender'],
                    receiver=t['receiver'],
                    amount=t['amount'],
                    date=t['date'],
                    transaction_type=t['transaction_type']
                )
                session.add(transaction)
        session.commit()
        logging.info(f"Loaded {len(transactions)} transactions into database")
    except Exception as e:
        session.rollback()
        logging.error(f"Error loading transactions: {str(e)}")
    finally:
        session.close()

if __name__ == '__main__':
    load_transactions('modified_sms_v2.xml')