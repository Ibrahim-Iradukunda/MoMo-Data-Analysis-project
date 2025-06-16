from flask import Flask, request, jsonify
from flask_cors import CORS
from process_sms import parse_sms_messages
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'momo.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        search = request.args.get('search', '').lower()
        
        if page < 1 or per_page < 1:
            return jsonify({'error': 'Invalid page or per_page value'}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        count_query = 'SELECT COUNT(*) FROM transactions WHERE date LIKE ? OR type LIKE ?'
        cursor.execute(count_query, (f'%{search}%', f'%{search}%'))
        total = cursor.fetchone()[0]
        
        offset = (page - 1) * per_page
        data_query = '''
            SELECT id, date, message, type, amount 
            FROM transactions 
            WHERE date LIKE ? OR type LIKE ?
            LIMIT ? OFFSET ?
        '''
        cursor.execute(data_query, (f'%{search}%', f'%{search}%', per_page, offset))
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        
        return jsonify({
            'data': data,
            'total': total,
            'page': page,
            'per_page': per_page
        })
    except ValueError:
        return jsonify({'error': 'Invalid page or per_page parameter'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)