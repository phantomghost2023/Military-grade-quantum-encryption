
from flask import Flask, request, jsonify
from src.auth import authenticate_user, generate_token, create_default_admin
from src.database import init_db
from src.data_manager import DataManager
from src.kms_api import KMS
from src.hybrid_crypto import HybridCrypto
from src.error_handling.error_handler import set_error_visualizer
from src.error_handling.error_visualizer import ErrorVisualizer
import base64
from src.api_versioning import create_api_blueprint
from src.input_validation import validate_string, sanitize_string, validate_email, validate_password
from src.logging_tracing import CentralizedLogger, DistributedTracer

app = Flask(__name__)

# Initialize Logger and Tracer
logger = CentralizedLogger()
tracer = DistributedTracer()


# Register API versions
app.register_blueprint(create_api_blueprint(1))
app.register_blueprint(create_api_blueprint(2))
data_manager = DataManager()
kms = KMS()
hybrid_crypto = HybridCrypto()

# Initialize error visualization
error_visualizer = ErrorVisualizer()
set_error_visualizer(error_visualizer)

@app.route('/api/auth/login', methods=['POST'])
def login():
    with tracer.start_span("login-request") as span:
        logger.info("Login attempt received.", remote_addr=request.remote_addr)
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        span.set_attribute("username", username)


    # Validate and sanitize username
    is_valid, msg = validate_string(username, min_length=3, max_length=50)
    if not is_valid:
        return jsonify({'message': f'Invalid username: {msg}'}), 400
    sanitized_username = sanitize_string(username)

    # Validate password (basic length check for now, more complex rules can be added)
    is_valid, msg = validate_password(password)
    if not is_valid:
        return jsonify({'message': f'Invalid password: {msg}'}), 400

    user = authenticate_user(sanitized_username, password)
    if user:
        token = generate_token(user['id'], user['username'], user['role'])
        logger.info("Login successful.", username=sanitized_username)
        span.set_attribute("login.status", "success")
        return jsonify({'message': 'Login successful', 'token': token})
    else:
        logger.warning("Login failed: Invalid credentials.", username=sanitized_username)
        span.set_attribute("login.status", "failed")
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

# --- KMS Endpoints ---

@app.route('/api/kms/generate_pqc_key', methods=['POST'])
def generate_pqc_key():
    # Authentication/Authorization would be added here
    data = request.get_json()
    key_id = data.get('key_id')
    algorithm = data.get('algorithm', 'Kyber') # Default to Kyber

    if not key_id:
        return jsonify({'message': 'Missing key_id'}), 400
    
    try:
        key_info = kms.generate_pqc_key_pair(key_id, algorithm)
        return jsonify({'message': 'PQC key pair generated successfully', 'key_info': key_info}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error generating PQC key: {e}'}), 500

@app.route('/api/kms/generate_symmetric_key', methods=['POST'])
def generate_symmetric_key():
    # Authentication/Authorization would be added here
    data = request.get_json()
    key_id = data.get('key_id')

    if not key_id:
        return jsonify({'message': 'Missing key_id'}), 400
    
    try:
        key_info = kms.generate_symmetric_key(key_id)
        return jsonify({'message': 'Symmetric key generated successfully', 'key_info': key_info}), 201
    except Exception as e:
        return jsonify({'message': f'Error generating symmetric key: {e}'}), 500


@app.route('/api/kms/rotate_key/<string:key_id>', methods=['POST'])
def rotate_key(key_id):
    # Authentication/Authorization would be added here
    try:
        new_key_id = kms.rotate_key(key_id)
        return jsonify({'message': f'Key {key_id} rotated successfully. New key ID: {new_key_id}'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error rotating key: {e}'}), 500

@app.route('/api/kms/revoke_key/<string:key_id>', methods=['POST'])
def revoke_key(key_id):
    # Authentication/Authorization would be added here
    try:
        kms.revoke_key(key_id)
        return jsonify({'message': f'Key {key_id} revoked successfully.'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error revoking key: {e}'}), 500

# --- Hybrid Crypto Endpoints ---

@app.route('/api/hybrid_crypto/key_exchange', methods=['POST'])
def hybrid_key_exchange():
    # Authentication/Authorization would be added here
    data = request.get_json()
    recipient_public_key_b64 = data.get('recipient_public_key')

    if not recipient_public_key_b64:
        return jsonify({'message': 'Missing recipient_public_key'}), 400

    try:
        recipient_public_key = base64.b64decode(recipient_public_key_b64)
        shared_secret, ciphertext, kms_pk = kms.perform_hybrid_key_exchange_with_kms(recipient_public_key)
        
        return jsonify({
            'message': 'Hybrid key exchange performed successfully',
            'shared_secret': base64.b64encode(shared_secret).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'kms_public_key': base64.b64encode(kms_pk).decode('utf-8')
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error during hybrid key exchange: {e}'}), 500

@app.route('/api/hybrid_crypto/encrypt', methods=['POST'])
def hybrid_encrypt():
    # Authentication/Authorization would be added here
    data = request.get_json()
    key_id = data.get('key_id')
    plaintext_b64 = data.get('plaintext')

    if not key_id or not plaintext_b64:
        return jsonify({'message': 'Missing key_id or plaintext'}), 400

    try:
        plaintext = base64.b64decode(plaintext_b64)
        ciphertext, nonce, tag = kms.encrypt_data_with_kms_key(key_id, plaintext)
        
        return jsonify({
            'message': 'Data encrypted successfully',
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8')
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error encrypting data: {e}'}), 500

@app.route('/api/hybrid_crypto/decrypt', methods=['POST'])
def hybrid_decrypt():
    # Authentication/Authorization would be added here
    data = request.get_json()
    key_id = data.get('key_id')
    ciphertext_b64 = data.get('ciphertext')
    nonce_b64 = data.get('nonce')
    tag_b64 = data.get('tag')

    if not all([key_id, ciphertext_b64, nonce_b64, tag_b64]):
        return jsonify({'message': 'Missing key_id, ciphertext, nonce, or tag'}), 400

    try:
        ciphertext = base64.b64decode(ciphertext_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)
        
        plaintext = kms.decrypt_data_with_kms_key(key_id, ciphertext, nonce, tag)
        
        return jsonify({
            'message': 'Data decrypted successfully',
            'plaintext': base64.b64encode(plaintext).decode('utf-8')
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error decrypting data: {e}'}), 500

@app.route('/api/hybrid_crypto/sign', methods=['POST'])
def hybrid_sign():
    # Authentication/Authorization would be added here
    data = request.get_json()
    key_id = data.get('key_id')
    message_b64 = data.get('message')

    if not key_id or not message_b64:
        return jsonify({'message': 'Missing key_id or message'}), 400

    try:
        message = base64.b64decode(message_b64)
        signature = kms.sign_data_with_kms_key(key_id, message)
        
        return jsonify({
            'message': 'Data signed successfully',
            'signature': base64.b64encode(signature).decode('utf-8')
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error signing data: {e}'}), 500

@app.route('/api/hybrid_crypto/verify', methods=['POST'])
def hybrid_verify():
    # Authentication/Authorization would be added here
    data = request.get_json()
    key_id = data.get('key_id')
    message_b64 = data.get('message')
    signature_b64 = data.get('signature')

    if not all([key_id, message_b64, signature_b64]):
        return jsonify({'message': 'Missing key_id, message, or signature'}), 400

    try:
        message = base64.b64decode(message_b64)
        signature = base64.b64decode(signature_b64)
        
        is_valid = kms.verify_data_with_kms_key(key_id, message, signature)
        
        return jsonify({
            'message': 'Signature verification complete',
            'is_valid': is_valid
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Error verifying signature: {e}'}), 500

if __name__ == '__main__':
    try:
        init_db()
        create_default_admin()
        logger.info("Starting API server...")
        app.run(debug=True, port=5000)
    except Exception as e:
        logger.critical(f"Failed to start API server: {e}")
        import sys
        sys.exit(1)
