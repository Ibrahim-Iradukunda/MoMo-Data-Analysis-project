import sqlite3

conn = sqlite3.connect('momo.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    message TEXT,
    type TEXT,
    amount INTEGER
)
''')

conn.commit()
conn.close()