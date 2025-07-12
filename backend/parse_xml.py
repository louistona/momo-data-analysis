import xml.etree.ElementTree as ET
from datetime import datetime
from data_cleaning import categorize_transaction, clean_amount, clean_date
import os

def parse_sms_xml(xml_file):
    transactions = []
    if not os.path.exists(xml_file):
        print(f"Error: XML file {xml_file} does not exist")
        return transactions

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        print(f"Found root element: {root.tag}")  # Debug print
        sms_elements = root.findall('sms')
        print(f"Found {len(sms_elements)} <sms> elements")  # Debug print

        for sms in sms_elements:
            try:
                # Extract data from attributes
                message = sms.get('body', '')
                sender = sms.get('address')
                # Extract receiver and amount from body (basic parsing)
                receiver = None
                amount = None
                if 'from' in message.lower():
                    # Example: "from Jane Smith (*********013)"
                    parts = message.split('from')
                    if '(' in parts[1]:
                        receiver = parts[1].split('(')[0].strip()
                elif 'to' in message.lower():
                    # Example: "to Jane Smith 12845"
                    parts = message.split('to')
                    receiver = parts[1].split()[0].strip()
                # Extract amount (e.g., "2000 RWF" or "1,000 RWF")
                if 'RWF' in message:
                    amount_str = message.split('RWF')[0].split()[-1].replace(',', '')
                    amount = clean_amount(amount_str)
                # Convert timestamp to datetime string for clean_date
                timestamp = sms.get('date')
                date_str = None
                if timestamp:
                    try:
                        date = datetime.fromtimestamp(int(timestamp) / 1000)
                        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass

                transaction = {
                    'message': message,
                    'sender': sender,
                    'receiver': receiver,
                    'amount': amount,
                    'date': clean_date(date_str) if date_str else None
                }
                transaction['transaction_type'] = categorize_transaction(transaction['message'])
                if transaction['transaction_type'] is None:
                    print(f"Unprocessed SMS: {transaction['message']}")
                    continue
                transactions.append(transaction)
            except Exception as e:
                print(f"Error processing SMS: {message}, Error: {str(e)}")
                continue
    except Exception as e:
        print(f"Error parsing XML file: {str(e)}")

    print(f"Parsed {len(transactions)} transactions")  # Debug print
    return transactions

if __name__ == '__main__':
    transactions = parse_sms_xml('modified_sms_v2.xml')
    print(f"Parsed {len(transactions)} transactions")