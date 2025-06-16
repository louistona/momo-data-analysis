import re
from datetime import datetime
import logging

def clean_amount(amount_str):
    if not amount_str:
        return None
    try:
        cleaned = re.sub(r'[^\d.]', '', amount_str)
        return int(float(cleaned))
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid amount format: {amount_str}, Error: {str(e)}")
        return None

def clean_date(date_str):
    if not date_str:
        return None
    try:
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        logging.error(f"Invalid date format: {date_str}")
        return None
    except Exception as e:
        logging.error(f"Error parsing date: {date_str}, Error: {str(e)}")
        return None

def categorize_transaction(message):
    if not message:
        return None
    message = message.lower()
    if 'received' in message:
        return 'Incoming Money'
    elif 'paid' in message or 'payment' in message:
        return 'Payments to Code Holders'
    elif 'transferred' in message or 'sent' in message:
        return 'Transfers to Mobile Numbers'
    elif 'bank deposit' in message:
        return 'Bank Deposits'
    elif 'airtime' in message:
        return 'Airtime Bill Payments'
    elif 'cash power' in message:
        return 'Cash Power Bill Payments'
    elif 'third party' in message:
        return 'Transactions Initiated by Third Parties'
    elif 'withdrawal' in message or 'withdraw' in message:
        return 'Withdrawals from Agents'
    elif 'bank transfer' in message:
        return 'Bank Transfers'
    elif 'internet' in message or 'voice bundle' in message:
        return 'Internet and Voice Bundle Purchases'
    else:
        return None