from process_sms import parse_sms
import sqlite3

# Parse data from XML
data = parse_sms('../data/momo_sms.xml')  # make sure path is correct

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
