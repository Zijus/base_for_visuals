from flask import Flask, request, jsonify
from functools import wraps
import sqlite3
import os

app = Flask(__name__)

# Basic Authentication
def check_auth(username, password):
    return username == os.environ.get('FLASK_USERNAME') and password == os.environ.get('FLASK_PASSWORD')

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Function to insert data into SQLite database
def insert_data(data):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            router TEXT,
            MQ2 REAL,
            MQ7 REAL,
            Flame REAL,
            UV REAL,
            CO REAL,
            CH4 REAL,
            Smoke REAL,
            Voltage REAL,
            Temperature REAL,
            Humidity REAL
        )
    ''')
    cursor.execute('''
        INSERT INTO sensor_data (router, MQ2, MQ7, Flame, UV, CO, CH4, Smoke, Voltage, Temperature, Humidity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['router'], data['MQ2'], data['MQ7'], data['Flame'], data['UV'], data['CO'], data['CH4'], data['Smoke'], data['Voltage'], data['Temperature'], data['Humidity']))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "Hello, this is the root URL of the Flask app!"

@app.route('/sensor', methods=['POST'])
@requires_auth
def sensor_data():
    data = request.json
    insert_data(data)
    return 'Data received', 200

if __name__ == '__main__':
    app.run(debug=True)
