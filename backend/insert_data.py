from process_sms import parse_sms_messages
import sqlite3
import os

# Path to XML file (adjust as needed)
XML_PATH = '../data/momo_sms.xml'

# Ensure XML file exists
if not os.path.exists(XML_PATH):
    print(f"Error: XML file not found at {XML_PATH}")
    exit(1)

# Parse data from XML
with open(XML_PATH, 'r', encoding='utf-8') as file:
    content = file.read()
    data = parse_sms_messages(content)

# Connect to DB
conn = sqlite3.connect('momo.db')
cursor = conn.cursor()

# Insert with amount column
cursor.executemany(
    'INSERT INTO transactions (date, message, type, amount) VALUES (?, ?, ?, ?)',
    data
)

conn.commit()
conn.close()
print(f"Successfully inserted {len(data)} transactions into the database")