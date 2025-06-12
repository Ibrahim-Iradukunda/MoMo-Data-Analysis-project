from flask import Flask, request, jsonify
from flask_cors import CORS
from process_sms import parse_sms_messages
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'momo.db'

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
    if not file.filename.endswith('.xml'):
        return jsonify({'message': 'Invalid file type. Please upload an XML file'}), 400

    try:
        content = file.read().decode('utf-8')
        transactions = parse_sms_messages(content)
        if not transactions:
            return jsonify({'message': 'No valid transactions found in the file'}), 400
        insert_messages_into_db(transactions)
        return jsonify({'message': f'Successfully processed {len(transactions)} transactions'})
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, date, message, type, amount FROM transactions')
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        data = [dict(zip(columns, row)) for row in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)