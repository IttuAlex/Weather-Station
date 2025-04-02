from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')  


CORS(app, resources={r"/*": {"origins": "http://100.72.182.23:*"}}, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

mongo_uri = os.getenv("MONGO_URI", "mongodb://100.72.182.23:27017/mydatabase")
client = MongoClient(mongo_uri)
db = client.mydatabase
collection = db.mycollection
collection2 = db.users
collection3 = db.messages  

online_users = {}

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = collection.insert_one(data)
        return jsonify({"message": "Data saved", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["GET"])
def get_data():
    try:
        document = collection.find_one(sort=[('_id', -1)], projection={'_id': 0})
        
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"error": "No data found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if collection2.find_one({'email': email}):
            return jsonify({'error': 'Email is already used'}), 409  

        hashed_password = generate_password_hash(password)  
        user_id = collection2.insert_one({'email': email, 'password': hashed_password}).inserted_id

        return jsonify({
            'message': 'Registration complete',
            'user_id': str(user_id)
        }), 201  

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = collection2.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            session['user'] = email
            session['user_id'] = str(user['_id'])

            return jsonify({
                'message': 'Login successful',
                'user': {'email': email, 'id': str(user['_id'])}
            }), 200
        
        return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = list(collection2.find({}, {"_id": 0, "email": 1}))
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/check_session", methods=["GET"])
def check_session():
    print(session)
    if 'user' in session:
        return jsonify({'logged_in': True}), 200
    return jsonify({'logged_in': False}), 401


@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        online_users[session['user_id']] = {
            'email': session['user'],
            'sid': request.sid
        }
        emit('online_users', list(online_users.values()), broadcast=True)
    else:
        disconnect()  


@socketio.on('disconnect')
def handle_disconnect():
    if 'user_id' in session and session['user_id'] in online_users:
        del online_users[session['user_id']]
        emit('online_users', list(online_users.values()), broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    if 'user_id' not in session:
        return
    
    message = data.get('message')
    recipient = data.get('recipient')  
    
    if not message:
        return
    
    message_data = {
        'sender': session['user_id'],
        'sender_email': session['user'],
        'message': message,
        'timestamp': datetime.now(),
        'recipient': recipient
    }
    
    collection3.insert_one(message_data)
    
    if recipient == 'all':
        emit('new_message', message_data, broadcast=True)
    else:
        if recipient in online_users:
            emit('new_message', message_data, room=online_users[recipient]['sid'])
        emit('new_message', message_data, room=request.sid)  


@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        limit = int(request.args.get('limit', 50))
        messages = list(collection3.find({
            '$or': [
                {'recipient': 'all'},
                {'recipient': session['user_id']},
                {'sender': session['user_id']}
            ]
        }).sort('timestamp', -1).limit(limit))
        
        for msg in messages:
            msg['_id'] = str(msg['_id'])
            msg['timestamp'] = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(messages[::-1])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
