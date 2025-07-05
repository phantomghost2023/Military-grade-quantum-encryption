from src.agent.base_agent import BaseAgent
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ErrorAgent(BaseAgent):
    """
    Agent responsible for handling errors and reporting them.
    """
    def __init__(self, agent_id):
        super().__init__(agent_id, capabilities=["ERROR_REPORTING", "LOG_ANALYSIS", "DIAGNOSE_ISSUE"])
        logging.info(f"ErrorAgent {self.agent_id} initialized.")

    def execute_task(self, task_payload):
        action = task_payload.get("action")
        error_code = task_payload.get("error_code")
        message = task_payload.get("message")

        if action == "report_error":
            logging.error(f"Error Agent {self.agent_id}: Reporting error {error_code} - {message}")
            # In a real system, this would integrate with an error logging/alerting system
            return {"status": "success", "message": f"Error {error_code} reported by {self.agent_id}."}
        elif action == "diagnose_issue":
            logging.info(f"Error Agent {self.agent_id}: Diagnosing issue {message}")
            # Simulate diagnosis
            return {"status": "success", "message": f"Issue diagnosed by {self.agent_id}. Root cause: simulated."}
        else:
            logging.warning(f"Error Agent {self.agent_id}: Unknown action {action}")
            return {"status": "failed", "message": f"Unknown action {action}"}
