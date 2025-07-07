import logging
import sys
import os
from flask import Flask, request, jsonify

# Add the project root to the sys.path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
from src.automation.automation_engine import AutomationEngine
from src.automation.policy_manager import PolicyManager
from src.automation.event_manager import EventManager
from src.automation.agent_manager import AgentManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Initialize core components
engine = AutomationEngine()
event_manager = EventManager(engine) # Pass engine to EventManager
agent_manager = AgentManager()
policy_manager = PolicyManager()

# Add default roles and permissions
policy_manager.add_role("default", ["create_task", "view_status"])

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
    Requires 'name', 'description', 'rules', and 'actions' in the request body.
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    rules = data.get('rules')
    actions = data.get('actions', [])

    if not name or not rules:
        return jsonify({"error": "'name' and 'rules' are required"}), 400

    # TODO: Implement proper permission check using the policy engine
    # if not engine.policy_engine.evaluate({"action_requested": "add_policy", "user_roles": user_roles}):
    #     return jsonify({"error": "Permission denied to add policies"}), 403

    engine.add_policy(name, description, rules, actions)
    event_manager.emit_event("policy_added", {"policy_name": name, "rules": rules, "actions": actions})
    return jsonify({"message": f"Policy '{name}' added"}), 201

@app.route('/api/v1/policies', methods=['GET'])
def get_policies_api():
    """
    Retrieves all policies.
    """
    policies = engine.get_policies()
    return jsonify({"policies": policies})

@app.route('/api/v1/policies/<policy_name>', methods=['GET'])
def get_policy_api(policy_name):
    """
    Retrieves a specific policy by name.
    """
    policy = engine.get_policy(policy_name)
    if policy:
        return jsonify({"policy": policy})
    return jsonify({"error": "Policy not found"}), 404

@app.route('/api/v1/policies/<policy_name>', methods=['PUT'])
def update_policy_api(policy_name):
    """
    Updates an existing policy.
    """
    data = request.get_json()
    new_description = data.get('description')
    new_rules = data.get('rules')
    new_actions = data.get('actions')

    # TODO: Implement proper permission check using the policy engine

    if engine.update_policy(policy_name, new_description, new_rules, new_actions):
        event_manager.emit_event("policy_updated", {"policy_name": policy_name})
        return jsonify({"message": f"Policy '{policy_name}' updated"})
    return jsonify({"error": "Policy not found"}), 404

@app.route('/api/v1/policies/<policy_name>', methods=['DELETE'])
def delete_policy_api(policy_name):
    """
    Deletes a policy.
    """
    # TODO: Implement proper permission check using the policy engine

    if engine.delete_policy(policy_name):
        event_manager.emit_event("policy_deleted", {"policy_name": policy_name})
        return jsonify({"message": f"Policy '{policy_name}' deleted"})
    return jsonify({"error": "Policy not found"}), 404

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

    # TODO: Implement proper permission check using the policy engine
    # if not engine.policy_engine.evaluate({"action_requested": "add_role", "user_roles": user_roles}):
    #     return jsonify({"error": "Permission denied to manage roles"}), 403

    # This functionality should ideally be moved to the PolicyEngine or a dedicated RoleManager
    # For now, we'll keep it here for demonstration purposes.
    # In a real system, roles would be managed more robustly.
    # For now, we'll just log it.
    logging.info(f"Attempting to add role: {role_name} with permissions: {permissions}")
    return jsonify({"message": f"Role '{role_name}' added (conceptual)"}), 201

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
    # Example initial policies and roles (these should be loaded from persistence)
    # For now, we'll just add a sample policy
    engine.add_policy(
        name="Allow_Admin_Task_Creation",
        description="Allows users with 'admin' role to create tasks.",
        rules={"action_requested": "create_task", "user_role": "admin"},
        actions=["allow_action"]
    )
    engine.add_policy(
        name="Allow_Admin_Policy_Management",
        description="Allows users with 'admin' role to manage policies.",
        rules={"action_requested": ["add_policy", "view_policies", "view_policy", "update_policy", "delete_policy"], "user_role": "admin"},
        actions=["allow_action"]
    )
    engine.add_policy(
        name="Allow_Admin_Role_Management",
        description="Allows users with 'admin' role to manage roles.",
        rules={"action_requested": "add_role", "user_role": "admin"},
        actions=["allow_action"]
    )
    engine.add_policy(
        name="Allow_Admin_Task_Control",
        description="Allows users with 'admin' role to view and cancel tasks.",
        rules={"action_requested": ["view_all_tasks", "cancel_task", "view_task_history", "list_available_tasks"], "user_role": "admin"},
        actions=["allow_action"]
    )
    engine.add_policy(
        name="Allow_Admin_Manual_Task_Trigger",
        description="Allows users with 'admin' role to manually trigger specific tasks.",
        rules={"action_requested": [f"trigger_task_{task_name}" for task_name in TASK_REGISTRY.keys()], "user_role": "admin"},
        actions=["allow_action"]
    )
    engine.add_policy(
        name="Allow_Default_View_Status",
        description="Allows users with 'default' role to view status.",
        rules={"action_requested": "view_status", "user_role": "default"},
        actions=["allow_action"]
    )

    # Register a simple event handler for task creation events
    def handle_task_created_event(payload):
        logging.info(f"API Interface: Received task_created event for task: {payload.get('task_name')}")
    event_manager.register_handler("task_created", handle_task_created_event)

    # Register KMS automation tasks to be triggered by events
    engine.register_event_task("key_expiration", automated_key_rotation, key_id="example_key_id") # Example: replace with actual key_id from event payload
    engine.register_event_task("key_revocation_request", automated_key_revocation, key_id="example_key_id") # Example
    engine.register_event_task("new_key_needed", automated_key_generation, key_type="hybrid") # Example

    # Register error automation tasks
    from src.automation.error_automation_tasks import automated_error_logging, automated_admin_notification, automated_system_restart_attempt
    engine.register_event_task("error_detected", automated_error_logging)
    engine.register_event_task("critical_error", automated_error_logging)
    engine.register_event_task("critical_error", automated_admin_notification)
    engine.register_event_task("critical_error", automated_system_restart_attempt)

    # Register error automation tasks
    from src.automation.error_automation_tasks import automated_error_logging, automated_admin_notification, automated_system_restart_attempt
    engine.register_event_task("error_detected", automated_error_logging)
    engine.register_event_task("critical_error", automated_error_logging)
    engine.register_event_task("critical_error", automated_admin_notification)
    engine.register_event_task("critical_error", automated_system_restart_attempt)

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