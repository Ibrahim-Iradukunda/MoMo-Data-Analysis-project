import xml.etree.ElementTree as ET
from datetime import datetime
import re

def parse_sms_messages(content):
    try:
        root = ET.fromstring(content)
        transactions = []

        for sms in root.findall('sms'):
            body = sms.get('body', '')
            if not body:
                continue  # Skip empty messages

            # Extract date from XML attribute
            date_ms = int(sms.get('date', '0'))
            date_str = (datetime.fromtimestamp(date_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
                       if date_ms else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # Determine transaction type with improved keyword matching
            body_lower = body.lower()
            if any(keyword in body_lower for keyword in ['airtime', 'bundle', 'recharge']):
                transaction_type = 'Airtime'
            elif 'withdrawn' in body_lower:
                transaction_type = 'Withdrawal'
            elif 'payment' in body_lower:
                transaction_type = 'Payment'
            elif 'received' in body_lower:
                transaction_type = 'Received'
            elif 'deposit' in body_lower:
                transaction_type = 'Deposit'
            elif any(keyword in body_lower for keyword in ['transfer', 'sent']):
                transaction_type = 'Transfer'
            else:
                transaction_type = 'Other'

            # Extract amount with fallback for malformed cases
            amount_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*RWF', body)
            amount = (int(amount_match.group(1).replace(',', '')) if amount_match 
                     else None)

            transactions.append((date_str, body, transaction_type, amount))

        return transactions
    except ET.ParseError:
        raise Exception("Invalid XML format")
    except Exception as e:
        raise Exception(f"Error parsing XML: {str(e)}")