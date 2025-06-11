import xml.etree.ElementTree as ET
from datetime import datetime
import re

def parse_sms(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []

    for sms in root.findall('sms'):
        body = sms.find('body').text if sms.find('body') is not None else ''
        
        # Sample fallback if using .get("body") (not recommended with your XML)
        if not body:
            body = sms.get('body', '')

        # Fake timestamp for now (if not in XML)
        date_match = re.search(r'Date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', body)
        if date_match:
            date_str = date_match.group(1)
        else:
            date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Determine transaction type
        if 'received' in body.lower():
            transaction_type = 'Received'
        elif 'withdrawn' in body.lower():
            transaction_type = 'Withdrawal'
        elif 'payment' in body.lower():
            transaction_type = 'Payment'
        elif 'airtime' in body.lower() or 'bundle' in body.lower():
            transaction_type = 'Airtime'
        else:
            transaction_type = 'Other'

        # Extract amount
        amount_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*RWF', body)
        amount = int(amount_match.group(1).replace(',', '')) if amount_match else None

        transactions.append((date_str, body, transaction_type, amount))

    return transactions
