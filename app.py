#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3 as sql

# declare Flask app and apply CORS to allow cross-origin requests
app = Flask(__name__)
CORS(app)

# connect to SQLite database
conn = sql.connect('slang.db')
conn.execute('''CREATE TABLE IF NOT EXISTS slang
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 term TEXT NOT NULL,
                 definition TEXT NOT NULL)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sql.connect('slang.db')
    cursor = conn.cursor()
    cursor.execute("SELECT term, definition FROM slang")
    slang_terms = cursor.fetchall()
    conn.close()

    slang_data = [{'term': term, 'definition': definition} for term, definition in slang_terms]
    return render_template('index.html', slang_data=slang_data)


@app.route('/add_slang', methods=['POST'])
def add_slang():
    '''Add a new slang term to the database'''
    data = request.get_json()
    term = data.get('term')
    definition = data.get('definition')

    if not term or not definition:
        return jsonify({'error': 'Term and definition are required'}), 400

    conn = sql.connect('slang.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO slang (term, definition) VALUES (?, ?)", (term, definition))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Slang term added successfully'}), 201

@app.route('/update_slang', methods=['POST'])
def update_slang():
    '''Update an existing slang term in the database'''
    data = request.get_json()
    term = data.get('term')
    definition = data.get('definition')

    if not term or not definition:
        return jsonify({'error': 'Term and definition are required'}), 400

    conn = sql.connect('slang.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE slang SET definition = ? WHERE term = ?", (definition, term))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Slang term updated successfully'}), 200

@app.route('/delete_slang', methods=['POST'])
def delete_slang():
    '''Delete a slang term from the database'''
    data = request.get_json()
    term = data.get('term')

    if not term:
        return jsonify({'error': 'Term is required'}), 400

    conn = sql.connect('slang.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM slang WHERE term = ?", (term,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Slang term deleted successfully'}), 200

@app.route('/search_slang', methods = ['GET'])
def search_slang():
    '''Search for slang terms in the database based on a query term'''
    term = request.args.get('term')
    conn = sql.connect('slang.db')
    cursor = conn.cursor()
    if term:
        cursor.execute("SELECT term, definition FROM slang WHERE term LIKE ?", ('%' + term + '%',))
    else:
        cursor.execute("SELECT term, definition FROM slang")
    slang_terms = cursor.fetchall()
    conn.close()

    slang_list = [{'term': term, 'definition': definition} for term, definition in slang_terms]
    return jsonify(slang_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)