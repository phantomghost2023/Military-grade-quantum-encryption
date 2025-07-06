
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

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    # In a real app, you'd add authentication/authorization here
    profile = data_manager.get_user_profile(user_id)
    if profile:
        return jsonify(profile)
    return jsonify({'message': 'Profile not found'}), 404

@app.route('/api/profile/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    # In a real app, you'd add authentication/authorization here
    data = request.get_json()
    display_name = data.get('display_name')
    profile_picture_url = data.get('profile_picture_url')
    preferences = data.get('preferences')

    updated = data_manager.update_user_profile(user_id, display_name, profile_picture_url, preferences)
    if updated:
        return jsonify({'message': 'Profile updated successfully'})
    return jsonify({'message': 'Profile update failed'}), 400

@app.route('/api/data', methods=['POST'])
def store_encrypted_data():
    # In a real app, you'd add authentication/authorization here
    data = request.get_json()
    user_id = data.get('user_id')
    data_type = data.get('data_type')
    encrypted_content = data.get('encrypted_content') # This would be base64 encoded string
    encryption_metadata = data.get('encryption_metadata')

    if not all([user_id, data_type, encrypted_content, encryption_metadata]):
        return jsonify({'message': 'Missing data'}), 400

    # Decode base64 content
    try:
        encrypted_content_bytes = base64.b64decode(encrypted_content)
    except Exception as e:
        return jsonify({'message': f'Invalid base64 content: {e}'}), 400

    data_id = data_manager.store_encrypted_data(user_id, data_type, encrypted_content_bytes, encryption_metadata)
    if data_id:
        return jsonify({'message': 'Data stored successfully', 'data_id': data_id}), 201
    return jsonify({'message': 'Failed to store data'}), 500

@app.route('/api/data/<data_id>', methods=['GET'])
def retrieve_encrypted_data(data_id):
    # In a real app, you'd add authentication/authorization here
    data = data_manager.retrieve_encrypted_data(data_id)
    if data:
        # Encode binary content back to base64 for JSON response
        data['encrypted_content'] = base64.b64encode(data['encrypted_content']).decode('utf-8')
        return jsonify(data)
    return jsonify({'message': 'Data not found'}), 404

@app.route('/api/data/<data_id>', methods=['DELETE'])
def delete_encrypted_data(data_id):
    # In a real app, you'd add authentication/authorization here
    deleted = data_manager.delete_encrypted_data(data_id)
    if deleted:
        return jsonify({'message': 'Data deleted successfully'})
    return jsonify({'message': 'Failed to delete data or data not found'}), 404

@app.route('/api/data/user/<int:user_id>', methods=['GET'])
def list_encrypted_data_by_user(user_id):
    # In a real app, you'd add authentication/authorization here
    data_type = request.args.get('data_type')
    data_list = data_manager.list_encrypted_data_by_user(user_id, data_type)
    return jsonify({'data_list': data_list})

if __name__ == '__main__':
    init_db()
    create_default_admin()
    app.run(debug=True, port=5000)
