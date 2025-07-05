import logging
import threading
import time
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgentManager:
    """
    Manages the registration, heartbeat, and task distribution for distributed agents.
    Agents are external services or modules that can execute tasks.
    """
    def __init__(self):
        self.agents = {}  # agent_id -> {info, last_heartbeat, status}
        self.agent_tasks = defaultdict(list) # agent_id -> [tasks_assigned]
        self.lock = threading.Lock() # Protects access to self.agents and self.agent_tasks
        self.heartbeat_monitor_thread = None
        self.is_monitoring = False
        logging.info("AgentManager initialized.")

    def register_agent(self, agent_id, agent_object, agent_info):
        """
        Registers a new agent or updates an existing agent's information.
        `agent_object`: The actual instance of the BaseAgent (or subclass).
        `agent_info`: Should contain details like capabilities (list of strings), endpoint, etc.
        """
        with self.lock:
            # Ensure 'capabilities' is a list, default to empty if not provided
            if 'capabilities' not in agent_info or not isinstance(agent_info['capabilities'], list):
                agent_info['capabilities'] = []

            self.agents[agent_id] = {
                "object": agent_object, # Store the actual agent object
                "info": agent_info,
                "last_heartbeat": time.time(),
                "status": "active",
                "load": 0 # Initialize load for task distribution
            }
            logging.info(f"Agent '{agent_id}' registered/updated with info: {agent_info}")

    def get_available_agents(self, required_capabilities=None, min_load=None, max_load=None):
        """
        Returns a dictionary of available agent objects, optionally filtered by capabilities and load.
        `required_capabilities`: A list of capabilities that agents must possess.
        `min_load`, `max_load`: Optional load thresholds.
        """
        with self.lock:
            available_agents = {}
            for agent_id, agent_data in self.agents.items():
                if agent_data["status"] == "active":
                    agent_info = agent_data["info"]
                    agent_capabilities = agent_info.get("capabilities", [])
                    agent_load = agent_data.get("load", 0)

                    # Check capabilities
                    if required_capabilities:
                        if not all(cap in agent_capabilities for cap in required_capabilities):
                            continue

                    # Check load
                    if min_load is not None and agent_load < min_load:
                        continue
                    if max_load is not None and agent_load > max_load:
                        continue

                    available_agents[agent_id] = agent_data["object"]
            return available_agents

    def get_agent(self, agent_id):
        """
        Returns the agent object for a given agent_id.
        """
        with self.lock:
            agent_data = self.agents.get(agent_id)
            return agent_data["object"] if agent_data else None

    def update_agent_load(self, agent_id, load_increment):
        """
        Updates the load of an agent. Use positive increment for assigning tasks, negative for completing.
        """
        with self.lock:
            if agent_id in self.agents:
                self.agents[agent_id]["load"] += load_increment
                if self.agents[agent_id]["load"] < 0:
                    self.agents[agent_id]["load"] = 0 # Ensure load doesn't go below zero
                logging.debug(f"Agent '{agent_id}' load updated to {self.agents[agent_id]["load"]}.")
            else:
                logging.warning(f"Attempted to update load for unknown agent '{agent_id}'.")

    def update_agent_status(self, agent_id, new_status):
        """
        Manually updates the status of an agent.
        """
        with self.lock:
            if agent_id in self.agents:
                self.agents[agent_id]["status"] = new_status
                logging.info(f"Agent '{agent_id}' status updated to '{new_status}'.")
            else:
                logging.warning(f"Attempted to update status for unknown agent '{agent_id}'.")

    def record_heartbeat(self, agent_id):
        """
        Records a heartbeat from an agent, indicating it's still active.
        """
        with self.lock:
            if agent_id in self.agents:
                self.agents[agent_id]["last_heartbeat"] = time.time()
                self.agents[agent_id]["status"] = "active"
                logging.debug(f"Heartbeat recorded for agent '{agent_id}'.")
            else:
                logging.warning(f"Heartbeat received from unknown agent '{agent_id}'.")

    def get_agent_status(self, agent_id):
        """
        Returns the status of a specific agent.
        """
        with self.lock:
            agent = self.agents.get(agent_id)
            return agent["status"] if agent else "not_found"

    def list_agents(self, status=None):
        """
        Lists all registered agents, optionally filtered by status.
        """
        with self.lock:
            if status:
                return {aid: a for aid, a in self.agents.items() if a["status"] == status}
            return self.agents.copy()

    def assign_task_to_agent(self, agent_id, task_payload):
        """
        Assigns a task to a specific agent.
        This would typically involve sending the task to the agent's endpoint.
        For now, we just record the assignment.
        """
        with self.lock:
            if agent_id in self.agents:
                self.agent_tasks[agent_id].append(task_payload)
                logging.info(f"Task assigned to agent '{agent_id}': {task_payload}")
                # In a real system, this would trigger an actual communication to the agent
                return True
            logging.warning(f"Attempted to assign task to unknown agent '{agent_id}'.")
            return False

    def _heartbeat_monitor_loop(self, timeout=30, check_interval=10):
        """
        Monitors agent heartbeats and updates their status to 'inactive' if timed out.
        """
        logging.info("Agent heartbeat monitor started.")
        while self.is_monitoring:
            current_time = time.time()
            with self.lock:
                for agent_id, agent_data in self.agents.items():
                    if agent_data["status"] == "active" and (current_time - agent_data["last_heartbeat"]) > timeout:
                        agent_data["status"] = "inactive"
                        logging.warning(f"Agent '{agent_id}' timed out. Status set to 'inactive'.")
            time.sleep(check_interval)
        logging.info("Agent heartbeat monitor stopped.")

    def start_monitoring(self):
        """
        Starts the heartbeat monitoring thread.
        """
        if not self.is_monitoring:
            self.is_monitoring = True
            self.heartbeat_monitor_thread = threading.Thread(target=self._heartbeat_monitor_loop)
            self.heartbeat_monitor_thread.daemon = True # Allow main program to exit even if this thread is running
            self.heartbeat_monitor_thread.start()
            logging.info("AgentManager monitoring started.")
        else:
            logging.info("AgentManager monitoring is already running.")

    def stop_monitoring(self):
        """
        Stops the heartbeat monitoring thread.
        """
        if self.is_monitoring:
            logging.info("Stopping AgentManager monitoring...")
            self.is_monitoring = False
            if self.heartbeat_monitor_thread and self.heartbeat_monitor_thread.is_alive():
                self.heartbeat_monitor_thread.join(timeout=5) # Give it some time to shut down
            logging.info("AgentManager monitoring stopped.")
        else:
            logging.info("AgentManager monitoring is not running.")

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    agent_manager = AgentManager()
    agent_manager.start_monitoring()

    # Register some agents with capabilities
    agent_manager.register_agent("kms_agent_001", None, {"type": "KMS", "location": "datacenter_a", "capabilities": ["KEY_ROTATION", "KEY_GENERATION"]})
    agent_manager.register_agent("error_agent_001", None, {"type": "ErrorHandler", "version": "1.0", "capabilities": ["ERROR_REPORTING", "LOG_ANALYSIS"]})
    agent_manager.register_agent("pqc_agent_001", None, {"type": "PQC", "hardware_id": "XYZ789", "capabilities": ["PQC_ENCRYPT_KYBER", "PQC_SIGN_DILITHIUM"]})
    agent_manager.register_agent("pqc_agent_002", None, {"type": "PQC", "hardware_id": "ABC123", "capabilities": ["PQC_ENCRYPT_KYBER"], "load": 5}) # Simulate higher initial load

    print("\n--- Registered Agents ---")
    print(agent_manager.list_agents())

    # Simulate heartbeats
    time.sleep(2)
    agent_manager.record_heartbeat("kms_agent_001")
    print(f"\nStatus of KMS Agent 001: {agent_manager.get_agent_status('kms_agent_001')}")

    # Assign a task and update load
    agent_manager.assign_task_to_agent("kms_agent_001", {"action": "rotate_key", "key_id": "key123"})
    agent_manager.update_agent_load("kms_agent_001", 1)
    agent_manager.assign_task_to_agent("error_agent_001", {"action": "diagnose_error", "error_code": "E001"})
    agent_manager.update_agent_load("error_agent_001", 1)

    print("\n--- Agent Tasks and Loads ---")
    with agent_manager.lock:
        print(agent_manager.agent_tasks)
        print({aid: a["load"] for aid, a in agent_manager.agents.items()})

    # Get available agents based on capabilities and load
    print("\n--- Available PQC Encryption Agents (low load) ---")
    pqc_encrypt_agents = agent_manager.get_available_agents(required_capabilities=["PQC_ENCRYPT_KYBER"], max_load=2)
    print(pqc_encrypt_agents)

    print("\n--- Available PQC Signing Agents ---")
    pqc_sign_agents = agent_manager.get_available_agents(required_capabilities=["PQC_SIGN_DILITHIUM"])
    print(pqc_sign_agents)

    # Simulate task completion and load reduction
    agent_manager.update_agent_load("kms_agent_001", -1)
    print(f"\nKMS Agent 001 load after task completion: {agent_manager.agents['kms_agent_001']['load']}")

    # Wait for an agent to time out (if timeout is short enough)
    print("\n--- Waiting for agent timeout (approx 35 seconds) ---")
    time.sleep(35) # Wait longer than default timeout (30s)
    print(f"Status of PQC Agent 001 after timeout: {agent_manager.get_agent_status('pqc_agent_001')}")

    agent_manager.stop_monitoring()
    print("\n--- Final Agent Statuses ---")
    print(agent_manager.list_agents())