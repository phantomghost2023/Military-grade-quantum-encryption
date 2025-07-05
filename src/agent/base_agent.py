import requests
import time
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseAgent:
    """
    Base class for all distributed agents. Handles registration, heartbeats,
    and task execution communication with the central AutomationEngine.
    """
    def __init__(self, agent_id, capabilities, ccu_api_endpoint="http://localhost:5000/api/agent"): # Placeholder endpoint
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.ccu_api_endpoint = ccu_api_endpoint
        self.is_running = False
        self.heartbeat_thread = None
        logging.info(f"Agent {self.agent_id} initialized with capabilities: {self.capabilities}")

    def _send_heartbeat(self):
        """
        Sends a heartbeat to the CCU.
        """
        try:
            # In a real system, this would be a POST request to the CCU's AgentManager API
            # For now, we'll simulate it by directly calling the AgentManager's record_heartbeat method
            # This requires the AutomationEngine to expose its AgentManager instance, which is not ideal for distributed systems
            # A proper API interface (e.g., REST, gRPC) would be implemented here.
            logging.debug(f"Agent {self.agent_id} sending heartbeat.")
            # Example of what a real API call might look like:
            # response = requests.post(f"{self.ccu_api_endpoint}/heartbeat", json={"agent_id": self.agent_id})
            # response.raise_for_status()
            # logging.debug(f"Heartbeat sent successfully for {self.agent_id}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send heartbeat for agent {self.agent_id}: {e}")

    def _heartbeat_loop(self, interval=10):
        """
        Continuously sends heartbeats to the CCU.
        """
        while self.is_running:
            self._send_heartbeat()
            time.sleep(interval)

    def register(self):
        """
        Registers the agent with the CCU.
        """
        try:
            logging.info(f"Agent {self.agent_id} attempting to register with CCU.")
            # In a real system, this would be a POST request to the CCU's AgentManager API
            # For now, we'll simulate it.
            # response = requests.post(f"{self.ccu_api_endpoint}/register", json={
            #     "agent_id": self.agent_id,
            #     "capabilities": self.capabilities
            # })
            # response.raise_for_status()
            logging.info(f"Agent {self.agent_id} registered successfully.")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to register agent {self.agent_id}: {e}")
            return False

    def start(self):
        """
        Starts the agent's heartbeat thread and registers with the CCU.
        """
        if not self.is_running:
            if self.register():
                self.is_running = True
                self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
                self.heartbeat_thread.daemon = True
                self.heartbeat_thread.start()
                logging.info(f"Agent {self.agent_id} started.")
            else:
                logging.error(f"Agent {self.agent_id} could not start due to registration failure.")
        else:
            logging.info(f"Agent {self.agent_id} is already running.")

    def stop(self):
        """
        Stops the agent's heartbeat thread.
        """
        if self.is_running:
            logging.info(f"Stopping agent {self.agent_id}...")
            self.is_running = False
            if self.heartbeat_thread and self.heartbeat_thread.is_alive():
                self.heartbeat_thread.join(timeout=5)
            logging.info(f"Agent {self.agent_id} stopped.")
        else:
            logging.info(f"Agent {self.agent_id} is not running.")

    def execute_task(self, task_payload):
        """
        Executes a task received from the CCU. This method should be overridden by subclasses.
        """
        logging.info(f"Agent {self.agent_id} received task: {task_payload}")
        # Subclasses will implement actual task execution logic here
        raise NotImplementedError("Subclasses must implement execute_task method.")

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    class KMSAgent(BaseAgent):
        def __init__(self, agent_id):
            super().__init__(agent_id, capabilities=["KEY_ROTATION", "KEY_GENERATION"])

        def execute_task(self, task_payload):
            action = task_payload.get("action")
            key_id = task_payload.get("key_id")
            if action == "rotate_key":
                logging.info(f"KMS Agent {self.agent_id}: Rotating key {key_id}")
                time.sleep(1) # Simulate work
                return {"status": "success", "message": f"Key {key_id} rotated."}
            else:
                logging.warning(f"KMS Agent {self.agent_id}: Unknown action {action}")
                return {"status": "failed", "message": f"Unknown action {action}"}

    class PQCEncryptionAgent(BaseAgent):
        def __init__(self, agent_id):
            super().__init__(agent_id, capabilities=["PQC_ENCRYPT_KYBER", "PQC_SIGN_DILITHIUM"])

        def execute_task(self, task_payload):
            action = task_payload.get("action")
            algorithm = task_payload.get("algorithm")
            data = task_payload.get("data")

            if action == "encrypt_data":
                logging.info(f"PQC Agent {self.agent_id}: Encrypting data with {algorithm}")
                time.sleep(2) # Simulate encryption
                return {"status": "success", "message": f"Data encrypted with {algorithm}"}
            else:
                logging.warning(f"PQC Agent {self.agent_id}: Unknown action {action}")
                return {"status": "failed", "message": f"Unknown action {action}"}

    # --- Demonstration ---
    kms_agent = KMSAgent("agent_kms_001")
    pqc_agent = PQCEncryptionAgent("agent_pqc_001")

    kms_agent.start()
    pqc_agent.start()

    # Simulate receiving tasks from CCU
    print("\n--- Simulating Task Execution ---")
    kms_agent.execute_task({"action": "rotate_key", "key_id": "test_key_123"})
    pqc_agent.execute_task({"action": "encrypt_data", "algorithm": "Kyber", "data": "some_sensitive_data"})

    time.sleep(15) # Let heartbeats run for a bit

    kms_agent.stop()
    pqc_agent.stop()
