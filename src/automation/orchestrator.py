import logging
from src.automation.automation_engine import AutomationEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Orchestrator:
    """
    The Orchestrator defines and manages high-level workflows by leveraging
    the AutomationEngine, PolicyManager, and AgentManager.
    """
    def __init__(self, automation_engine: AutomationEngine):
        self.automation_engine = automation_engine
        logging.info("Orchestrator initialized.")

    def define_workflow(self, workflow_name, tasks):
        """
        Defines a new workflow.
        `tasks` is a list of dictionaries, each representing a task to be added to the AutomationEngine.
        Example task dictionary: {"function": func, "priority": 1, "required_capabilities": ["CAP"], "args": [], "kwargs": {}}
        """
        logging.info(f"Defining workflow: {workflow_name}")
        # In a real system, workflows would be persisted and more complex logic would be here
        # For now, we'll just store them as a simple dictionary
        self.automation_engine.policy_manager.add_policy(workflow_name, {"workflow_tasks": tasks})
        logging.info(f"Workflow '{workflow_name}' defined.")

    def execute_workflow(self, workflow_name, user_roles=["system"]):
        """
        Executes a defined workflow.
        """
        logging.info(f"Attempting to execute workflow: {workflow_name}")
        workflow_policy = self.automation_engine.policy_manager.get_policy(workflow_name)

        if not workflow_policy or "workflow_tasks" not in workflow_policy:
            logging.error(f"Workflow '{workflow_name}' not found or improperly defined.")
            return False

        # Check if the user/system has permission to execute this workflow
        if not self.automation_engine.policy_manager.check_permission(user_roles=user_roles, action="execute_workflow", resource=workflow_name):
            logging.warning(f"Execution of workflow '{workflow_name}' denied by policy for roles {user_roles}.")
            return False

        tasks_to_execute = workflow_policy["workflow_tasks"]
        task_ids = []
        for task_data in tasks_to_execute:
            # Ensure task_data has all necessary keys, provide defaults if missing
            func = task_data.get("function")
            priority = task_data.get("priority", 5)
            required_capabilities = task_data.get("required_capabilities")
            args = task_data.get("args", [])
            kwargs = task_data.get("kwargs", {})

            if func:
                task_id = self.automation_engine.add_task(func, priority=priority, required_capabilities=required_capabilities, *args, **kwargs)
                task_ids.append(task_id)
            else:
                logging.error(f"Invalid task definition in workflow '{workflow_name}': function missing.")
                return False
        logging.info(f"Workflow '{workflow_name}' tasks added to AutomationEngine: {task_ids}")
        return task_ids

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    from src.agent.kms_agent import KMSAgent
    from src.agent.pqc_agent import PQCAgent
    from src.agent.error_agent import ErrorAgent

    engine = AutomationEngine()
    engine.start()

    # Register concrete agent instances with the engine's agent_manager
    kms_agent = KMSAgent("kms_agent_001")
    pqc_agent = PQCAgent("pqc_agent_001")
    error_agent = ErrorAgent("error_agent_001")

    engine.agent_manager.register_agent(kms_agent.agent_id, kms_agent, kms_agent.capabilities)
    engine.agent_manager.register_agent(pqc_agent.agent_id, pqc_agent, pqc_agent.capabilities)
    engine.agent_manager.register_agent(error_agent.agent_id, error_agent, error_agent.capabilities)

    orchestrator = Orchestrator(engine)

    # Define a workflow for secure data encryption (using KMS and PQC agents)
    orchestrator.define_workflow(
        "SecureDataEncryption",
        [
            {"task_type": "KMS_KEY_ROTATION", "task_payload": {"action": "rotate_key", "key_id": "my_secret_key"}, "priority": 1, "required_capabilities": ["KMS_KEY_ROTATION"]},
            {"task_type": "PQC_ENCRYPT_DATA", "task_payload": {"action": "encrypt_data", "data": "sensitive_info", "algorithm": "Kyber"}, "priority": 2, "required_capabilities": ["PQC_ENCRYPT_KYBER"]}
        ]
    )

    # Define a workflow for error handling
    orchestrator.define_workflow(
        "HandleCriticalError",
        [
            {"task_type": "ERROR_REPORTING", "task_payload": {"action": "report_error", "error_code": "E007", "message": "Critical system failure"}, "priority": 1, "required_capabilities": ["ERROR_REPORTING"]},
            {"task_type": "DIAGNOSE_ISSUE", "task_payload": {"action": "diagnose_issue", "message": "System failure analysis"}, "priority": 2, "required_capabilities": ["DIAGNOSE_ISSUE"]}
        ]
    )

    # Execute the secure data encryption workflow
    print("\n--- Executing SecureDataEncryption Workflow ---")
    executed_task_ids_encryption = orchestrator.execute_workflow("SecureDataEncryption", user_roles=["admin"])
    print(f"Executed encryption task IDs: {executed_task_ids_encryption}")

    # Execute the error handling workflow
    print("\n--- Executing HandleCriticalError Workflow ---")
    executed_task_ids_error = orchestrator.execute_workflow("HandleCriticalError", user_roles=["admin"])
    print(f"Executed error handling task IDs: {executed_task_ids_error}")

    # Try to execute a workflow without permission
    print("\n--- Executing SecureDataEncryption Workflow (Denied) ---")
    orchestrator.execute_workflow("SecureDataEncryption", user_roles=["guest"])

    # Define a policy for workflow execution permission
    engine.policy_manager.add_role("admin", ["execute_workflow", "KMS_KEY_ROTATION", "PQC_ENCRYPT_DATA", "ERROR_REPORTING", "DIAGNOSE_ISSUE"])

    print("\n--- Executing SecureDataEncryption Workflow (Granted) ---")
    executed_task_ids_encryption_granted = orchestrator.execute_workflow("SecureDataEncryption", user_roles=["admin"])
    print(f"Executed encryption task IDs (granted): {executed_task_ids_encryption_granted}")

    print("\n--- Executing HandleCriticalError Workflow (Granted) ---")
    executed_task_ids_error_granted = orchestrator.execute_workflow("HandleCriticalError", user_roles=["admin"])
    print(f"Executed error handling task IDs (granted): {executed_task_ids_error_granted}")

    # Wait for tasks to complete
    import time
    time.sleep(5)

    engine.stop()
