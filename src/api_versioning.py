"""
Module for managing API versioning.
"""

from flask import Blueprint, request, jsonify

def create_api_blueprint(version):
    """
    Creates a Flask Blueprint for a specific API version.
    """
    blueprint = Blueprint(f'api_v{version}', __name__, url_prefix=f'/api/v{version}')

    @blueprint.route('/status', methods=['GET'])
    def status():
        return jsonify({"version": version, "status": "active", "message": f"Welcome to API Version {version}"})

    # Example of a versioned endpoint
    @blueprint.route('/data', methods=['GET'])
    def get_data():
        # In a real application, this would fetch data specific to this API version
        return jsonify({"version": version, "data": ["item1_v" + str(version), "item2_v" + str(version)]})

    return blueprint

# Example Usage (for demonstration, not part of the core library)
if __name__ == '__main__':
    from flask import Flask

    app = Flask(__name__)

    # Register different API versions
    app.register_blueprint(create_api_blueprint(1))
    app.register_blueprint(create_api_blueprint(2))

    @app.route('/')
    def index():
        return "Welcome to the API Gateway. Try /api/v1/status or /api/v2/status"

    app.run(debug=True, port=5000)