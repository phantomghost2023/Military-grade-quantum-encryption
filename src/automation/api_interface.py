import logging
import sys
import os
from flask import Flask, request, jsonify

# Add the project root to the sys.path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
from automation.automation_engine import AutomationEngine
from automation.policy_manager import PolicyManager
from automation.event_manager import EventManager
from automation.agent_manager import AgentManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Initialize core components
engine = AutomationEngine()
policy_manager = PolicyManager()
event_manager = EventManager()
agent_manager = AgentManager()

# Start the engine and event manager worker threads
engine.start()
event_manager.start()
agent_manager.start_monitoring()

# --- API Endpoints ---

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """
    Returns the current status of the automation system.
    """
    return jsonify({
        "engine_status": "running" if engine.is_running else "stopped",
        "event_manager_status": "running" if event_manager.is_running else "stopped",
        "queued_tasks": engine.list_tasks()["queued"],
        "running_tasks": engine.list_tasks()["running"]
    })

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    """
    Submits a new automation task.
    Requires 'task_function_name' and 'args' in the request body.
    """
    data = request.get_json()
    task_function_name = data.get('task_function_name')
    task_args = data.get('args', [])
    task_kwargs = data.get('kwargs', {})
    user_roles = data.get('user_roles', ['default'])

    if not task_function_name:
        return jsonify({"error": "'task_function_name' is required"}), 400

    # Basic permission check (can be expanded)
    if not policy_manager.check_permission(user_roles, 'create_task'):
        return jsonify({"error": "Permission denied to create tasks"}), 403

    # In a real application, you would map task_function_name to actual callable functions
    # For this example, we'll use a placeholder or a simple lookup
    def placeholder_task(*args, **kwargs):
        logging.info(f"Executing placeholder task: {task_function_name} with args {args}, kwargs {kwargs}")
        # Simulate work
        import time
        time.sleep(1)
        return f"Task {task_function_name} completed."

    # Emit an event for task creation
    event_manager.emit_event("task_created", {
        "task_name": task_function_name,
        "args": task_args,
        "kwargs": task_kwargs,
        "user_roles": user_roles
    })

    task_id = engine.add_task(placeholder_task, *task_args, **task_kwargs)
    return jsonify({"message": "Task submitted", "task_id": task_id}), 202

@app.route('/api/v1/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    Retrieves the status of a specific task.
    """
    status = engine.get_task_status(task_id)
    if status == "not_found":
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task_id": task_id, "status": status})

@app.route('/api/v1/policies', methods=['POST'])
def add_policy_api():
    """
    Adds a new policy.
    Requires 'policy_name' and 'rules' in the request body.
    """
    data = request.get_json()
    policy_name = data.get('policy_name')
    rules = data.get('rules')
    user_roles = data.get('user_roles', ['default'])

    if not policy_name or not rules:
        return jsonify({"error": "'policy_name' and 'rules' are required"}), 400

    if not policy_manager.check_permission(user_roles, 'manage_policies'):
        return jsonify({"error": "Permission denied to manage policies"}), 403

    policy_manager.add_policy(policy_name, rules)
    event_manager.emit_event("policy_added", {"policy_name": policy_name, "rules": rules})
    return jsonify({"message": f"Policy '{policy_name}' added"}), 201

@app.route('/api/v1/roles', methods=['POST'])
def add_role_api():
    """
    Adds a new role with permissions.
    Requires 'role_name' and 'permissions' in the request body.
    """
    data = request.get_json()
    role_name = data.get('role_name')
    permissions = data.get('permissions')
    user_roles = data.get('user_roles', ['default'])

    if not role_name or not permissions:
        return jsonify({"error": "'role_name' and 'permissions' are required"}), 400

    if not policy_manager.check_permission(user_roles, 'manage_roles'):
        return jsonify({"error": "Permission denied to manage roles"}), 403

    policy_manager.add_role(role_name, permissions)
    event_manager.emit_event("role_added", {"role_name": role_name, "permissions": permissions})
    return jsonify({"message": f"Role '{role_name}' added"}), 201

# Agent Management Endpoints
@app.route('/api/v1/agents', methods=['GET'])
def list_agents():
    status_filter = request.args.get('status')
    agents = agent_manager.list_agents(status=status_filter)
    return jsonify({'agents': agents})

@app.route('/api/v1/agents/<agent_id>', methods=['POST'])
def register_agent(agent_id):
    agent_info = request.get_json()
    if not agent_info:
        return jsonify({'error': 'Agent info required'}), 400
    
    agent_manager.register_agent(agent_id, agent_info)
    return jsonify({'status': 'success'}), 201

@app.route('/api/v1/agents/<agent_id>/heartbeat', methods=['POST'])
def record_heartbeat(agent_id):
    agent_manager.record_heartbeat(agent_id)
    return jsonify({'status': 'success'})

@app.route('/api/v1/agents/<agent_id>/tasks', methods=['POST'])
def assign_task(agent_id):
    task_payload = request.get_json()
    if not task_payload:
        return jsonify({'error': 'Task payload required'}), 400
    
    success = agent_manager.assign_task_to_agent(agent_id, task_payload)
    if not success:
        return jsonify({'error': 'Agent not found'}), 404
    
    return jsonify({'status': 'success'}), 201


if __name__ == '__main__':
    # Example initial policies and roles
    policy_manager.add_policy("default_task_creation", {"allow": ["create_task"]})
    policy_manager.add_role("default", ["create_task", "view_status"])
    policy_manager.add_role("admin", ["*", "manage_policies", "manage_roles"])

    # Register a simple event handler for task creation events
    def handle_task_created_event(payload):
        logging.info(f"API Interface: Received task_created event for task: {payload.get('task_name')}")
    event_manager.register_handler("task_created", handle_task_created_event)

    # Run the Flask app
    # In a production environment, use a more robust WSGI server like Gunicorn or uWSGI
    app.run(debug=True, port=5000)

# Graceful shutdown (optional, for more robust applications)
# You might want to add a signal handler to stop engine and event_manager cleanly
# For example:
# import atexit
# @atexit.register
# def shutdown_components():
#     engine.stop()
#     event_manager.stop()
#     logging.info("Automation components gracefully shut down.")