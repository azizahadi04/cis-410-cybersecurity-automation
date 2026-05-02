import os
import sqlite3
import socket
import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY, username TEXT, email TEXT, role TEXT, department TEXT
    )''')
    conn.executemany('INSERT INTO users VALUES (?,?,?,?,?)', [
        (1,'alice',  'alice@corp.local',  'admin',  'Engineering'),
        (2,'bob',    'bob@corp.local',    'user',   'Marketing'),
        (3,'charlie','charlie@corp.local','user',   'Finance'),
        (4,'diana',  'diana@corp.local',  'manager','Engineering'),
        (5,'eve',    'eve@corp.local',    'admin',  'Security'),
        (6,'frank',  'frank@corp.local',  'user',   'HR'),
    ])
    conn.commit()
    return conn

DB = init_db()

def ctx():
    return {
        'hostname':    socket.gethostname(),
        'environment': os.environ.get('ENVIRONMENT', 'dev'),
        'version':     os.environ.get('APP_VERSION', '2.0.0-secure'),
        'deploy_time': os.environ.get('DEPLOY_TIME', 'unknown'),
        'commit_sha':  os.environ.get('COMMIT_SHA', 'local')[:7],
        'port':        os.environ.get('HOST_PORT', '5000'),
    }

@app.route('/')
def index():
    return render_template('index.html', **ctx())

# ✅ FIXED: SQL Injection removed (parameterized query)
@app.route('/search')
def search():
    q = request.args.get('q', '')
    results, error = [], None
    if q:
        try:
            cursor = DB.execute(
                "SELECT * FROM users WHERE username = ?", (q,)
            )
            results = cursor.fetchall()
        except Exception as e:
            error = str(e)
    return render_template('search.html', q=q, results=results, error=error, **ctx())

# ❌ Removed insecure debug endpoint

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'app': 'secure',
        'version': os.environ.get('APP_VERSION', '2.0.0-secure'),
        'env': os.environ.get('ENVIRONMENT', 'dev'),
        'host': socket.gethostname(),
        'time': datetime.datetime.utcnow().isoformat() + 'Z',
    })

if __name__ == '__main__':
    # ✅ FIXED: debug disabled
    app.run(host='0.0.0.0', port=5000, debug=False)
