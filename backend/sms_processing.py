import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from functools import reduce
from uuid import UUID, uuid4

from sqlmodel import Date, Field, Session, SQLModel, cast, col, select, text

log_file = "unprocessed_sms.log"

logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SmsData(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, unique=True, nullable=False
    )
    address: str = Field(nullable=True)
    date_sent: datetime = Field(nullable=True)
    message: str = Field(nullable=True)
    service_center: str = Field(nullable=True)
    amount: float = Field(nullable=True)
    message_type: str = Field(nullable=True)
    category: str = Field(nullable=True)
    date: datetime = Field(nullable=True)

    @staticmethod
    def search():
        return [
            SmsData.address,
            SmsData.message,
            SmsData.service_center,
            SmsData.message_type,
            SmsData.category,
        ]


class SMSProcessor:
    """This class is for parsing, cleaning and storing
    data in the db, it contains a method for creating a db connection
    """

    DEFAULT_XML = "modified_sms_v2.xml"

    def __init__(self, db: Session, xml_file=DEFAULT_XML, log_file=log_file):
        """
        Initialize the SMSProcessor with an XML file, database configuration, and a log file.

        Args:
            xml_file (str): Path to the XML file.
            db_config (dict): Database configuration with keys 'host', 'user', 'password', 'database'.
            log_file (str): Path to the log file for unprocessed SMS messages.
        """

        self.xml_file = xml_file
        self.db = db
        self.log_file = log_file

    def parse_message(self, message):
        """
        Parse the message to extract amount, message_type, and category.

        Args:
            message (str): The SMS message content.

        Returns:
            tuple: Extracted (amount, message_type, category). Returns (None, None, None) if parsing fails.
        """
        amount = None
        message_type_ = None
        category = None

        try:
            # Extract amount associated with each transaction
            amount_search = re.search(r"(\d+(?:,\d{3})*)\s*RWF", message)

            if amount_search:

                amount = float(amount_search.group(1).replace(",", ""))
            else:
                amount = None

            # Determine type and category based on keywords
            # Incoming Money
            if "received" in message.lower():
                category = "Coming"
                message_type_ = "Incoming Money"

            # Transfers To Mobile Numbers
            elif "transferred" in message.lower():
                category = "Going"
                message_type_ = "Transfers To Mobile Numbers"

            # Payments to Code Holders
            elif "payment" in message.lower():
                category = "Going"
                message_type_ = "Payments to Code Holders"

            # Bank Deposits
            elif "bank deposit" in message.lower():
                category = "Coming"
                message_type_ = "Bank Deposits"

            # Airtime Bill Payments
            elif "to Airtime" in message.lower():
                category = "Going"
                message_type_ = "Airtime Bill Payments"

            # Cash Power Bill Payments
            elif "Cash Power" in message.lower():
                category = "Going"
                message_type_ = "Cash Power Bill Payments"

            # Transactions Initiated by Third Parties
            elif "a transaction of" in message.lower():
                category = "Going"
                message_type_ = "Transactions Initiated by Third Parties"

            # Withdrawals from Agents
            elif "agent" in message.lower():
                category = "Going"
                message_type_ = "Withdrawals from Agents"

            # Internet and Voice Bundle Purchases
            elif "kugura" in message.lower():
                category = "Going"
                message_type_ = "Internet and Voice Bundle Purchases"

            elif "failed" in message.lower():
                category = "No change"
                message_type_ = "Failed Transactions"

            elif "reversed" in message.lower() or "reversal" in message.lower():
                category = "both ways"
                message_type_ = "Reversed Transactions"

            else:
                category = "Unknown"
                message_type_ = "Unknown"
        except Exception as e:
            logging.warning(f"Error parsing message: {message}. Error: {e}")
        return amount, message_type_, category

    def is_duplicates(self, message, date, date_sent) -> bool:
        """Check if the SMS already exists in the database to avoid duplicates."""

        query = select(SmsData).where(
            SmsData.message == message,
            SmsData.date == date,
            SmsData.date_sent == date_sent,
        )

        result = self.db.exec(query).first()

        return result if result else False

    def process_and_store_sms(self):
        """Parse the XML file and store SMS data into the database."""
        try:
            logging.info(f"Starting to process SMS data from {self.xml_file}")
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            processed_count = 0
            skipped_count = 0
            
            for sms in root.findall("sms"):
                try:
                    address = sms.attrib.get("address", "")
                    message = sms.attrib.get("body", "")
                    service_center = sms.attrib.get("service_center", "")
                    date = datetime.fromtimestamp(
                        int(sms.attrib["date"]) / 1000
                    ).strftime("%Y-%m-%d%H:%M:%S")
                    date_sent = datetime.fromtimestamp(
                        int(sms.attrib["date_sent"]) / 1000
                    ).strftime("%Y-%m-%d%H:%M:%S")

                    date = datetime.strptime(date, "%Y-%m-%d%H:%M:%S")
                    date_sent = datetime.strptime(date_sent, "%Y-%m-%d%H:%M:%S")

                    # Parse message to extract additional fields
                    amount, message_type_, category = self.parse_message(message)
                    if message_type_ == "Unknown":
                        # Log unprocessed messages
                        logging.warning(f"Unprocessed message: {message}")
                        with open(self.log_file, "a") as log:
                            log.write(f"{sms.attrib}\n")
                        skipped_count += 1
                        continue

                    if self.is_duplicates(message, date, date_sent):
                        logging.warning(
                            f"Duplicate SMS detected and skipped: {message}"
                        )
                        skipped_count += 1
                        continue

                    # Insert into the database
                    add_sms = SmsData(
                        address=address,
                        date_sent=date_sent,
                        date=date,
                        message=message,
                        service_center=service_center,
                        amount=amount,
                        message_type=message_type_,
                        category=category,
                    )
                    self.db.add(add_sms)
                    self.db.commit()
                    processed_count += 1
                    
                    logging.info(f"Processed SMS: {message} - Type: {message_type_}")
                except Exception as e:
                    logging.error(f"Error processing SMS: {e}")
                    self.db.rollback()
                    continue
            
            logging.info(f"Processing complete. Processed: {processed_count}, Skipped: {skipped_count}")
            return {"message": "Data stored successfully", 
                   "processed": processed_count, 
                   "skipped": skipped_count}
        except Exception as e:
            logging.error(f"Error processing XML file: {e}")
            return {"error": f"Failed to process XML file: {str(e)}"}

    def data(self):
        try:
            # Get all SMS data from the database
            results = self.db.exec(select(SmsData)).all()
            return results
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            return []


def get_search_query(table_model, search: str):
    search_where = list(
        map(lambda x: col(x).ilike(f"%{search}%"), table_model.search())
    )
    return reduce(lambda x, y: x | y, search_where)


def get_all_sms(
    db: Session,
    search,
    type,
    date,
    amount,
):
    fetching_query = []

    if type:
        fetching_query.append(SmsData.message_type == type)
    # Add date filter
    if date:
        fetching_query.append(cast(SmsData.date, Date) == date)
    if amount:
        fetching_query.append(SmsData.amount == amount)

    if search and len(search) > 0:
        search_query = get_search_query(SmsData, search)
        fetching_query.append(search_query)

    return db.exec(select(SmsData).where(*fetching_query)).all()
