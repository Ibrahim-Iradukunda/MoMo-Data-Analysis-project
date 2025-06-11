from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import xml.etree.ElementTree as ET
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

DB_PATH = 'momo.db'

def parse_sms_messages(content):
    root = ET.fromstring(content)
    transactions = []

    for sms in root.findall('sms'):
        body = sms.get('body', '')
        date_ms = int(sms.get('date', '0'))
        date_str = datetime.fromtimestamp(date_ms / 1000).strftime('%Y-%m-%d %H:%M:%S') if date_ms else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

def insert_messages_into_db(transactions):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO transactions (date, message, type, amount) VALUES (?, ?, ?, ?)', transactions)
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload_xml():
    file = request.files.get('file')
    if not file:
        return jsonify({'message': 'No file provided'}), 400

    content = file.read()
    try:
        messages = parse_sms_messages(content)
        insert_messages_into_db(messages)
        return jsonify({'message': 'File uploaded and processed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    rows = c.fetchall()
    columns = [description[0] for description in c.description]
    conn.close()

    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
