
from flask import Flask, request, jsonify
from src.auth import authenticate_user, generate_token, create_default_admin
from src.database import init_db

app = Flask(__name__)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = authenticate_user(username, password)
    if user:
        token = generate_token(user['id'], user['username'], user['role'])
        return jsonify({'message': 'Login successful', 'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    init_db()
    create_default_admin()
    app.run(debug=True, port=5000)
