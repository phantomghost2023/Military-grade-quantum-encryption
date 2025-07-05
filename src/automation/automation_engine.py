import threading
import time
import logging
import heapq # For priority queue
from collections import deque # Still useful for running tasks
from src.automation.policy_manager import PolicyManager # Import PolicyManager
from src.automation.agent_manager import AgentManager # Import AgentManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomationEngine:
    """
    The core automation engine responsible for managing and executing tasks.
    It handles task scheduling, execution, and basic error handling.
    """
    def __init__(self):
        self.task_queue = []  # Stores tasks to be executed as a min-heap (priority, task_id, task)
        self.running_tasks = {}  # Stores currently running tasks
        self.task_id_counter = 0
        self.is_running = False
        self.worker_thread = None
        self.policy_manager = PolicyManager() # Initialize PolicyManager
        self.agent_manager = AgentManager() # Initialize AgentManager
        logging.info("AutomationEngine initialized.")

    def _generate_task_id(self):
        self.task_id_counter += 1
        return f"task_{self.task_id_counter}"

    def add_task(self, task_type, task_payload, priority=5, required_capabilities=None):
        """
        Adds a new task to the automation engine's queue with a given priority.
        Lower priority number means higher priority.
        `task_type`: A string identifying the type of task (e.g., "KMS_KEY_ROTATION", "PQC_ENCRYPT").
        `task_payload`: A dictionary containing all necessary arguments for the agent to execute the task.
        `required_capabilities`: List of capabilities an agent needs to execute this task.
        """
        task_id = self._generate_task_id()
        task = {
            "id": task_id,
            "type": task_type,
            "payload": task_payload,
            "status": "queued",
            "priority": priority,
            "required_capabilities": required_capabilities
        }
        heapq.heappush(self.task_queue, (priority, task_id, task))
        logging.info(f"Task '{task_id}' (type: {task_type}) added to queue with priority {priority}. Required capabilities: {required_capabilities}")
        return task_id

    def _execute_task(self, task):
        """
        Executes a single task by dispatching it to a suitable agent and updates its status.
        Includes policy pre-checks and agent selection/load management.
        """
        task_id = task["id"]
        task_type = task["type"]
        task_payload = task["payload"]
        required_capabilities = task.get("required_capabilities")

        # Policy Pre-check
        # The action for policy check is now the task_type
        if not self.policy_manager.check_permission(user_roles=["system"], action=task_type, resource=None, **task_payload):
            task["status"] = "denied_by_policy"
            logging.warning(f"Task '{task_id}' (type: {task_type}) denied by policy.")
            return None

        # Agent Selection
        selected_agent_id = None
        selected_agent_object = None
        if required_capabilities:
            available_agents = self.agent_manager.get_available_agents(required_capabilities=required_capabilities)
            if not available_agents:
                task["status"] = "no_suitable_agent"
                logging.warning(f"Task '{task_id}' (type: {task_type}) could not find a suitable agent with capabilities {required_capabilities}.")
                return None
            
            # Simple agent selection: pick the least loaded available agent
            # available_agents now contains agent objects directly
            selected_agent_id = min(available_agents, key=lambda agent_id: available_agents[agent_id].load) # Assuming agent objects have a 'load' attribute
            selected_agent_object = available_agents[selected_agent_id]
            
            self.agent_manager.update_agent_load(selected_agent_id, 1) # Increment agent load
            logging.info(f"Task '{task_id}' assigned to agent '{selected_agent_id}'.")
        else:
            task["status"] = "no_agent_specified"
            logging.warning(f"Task '{task_id}' (type: {task_type}) has no required capabilities specified. Cannot dispatch to agent.")
            return None

        logging.info(f"Executing task '{task_id}' (type: {task_type}) on agent '{selected_agent_id}'...")
        task["status"] = "running"
        self.running_tasks[task_id] = task

        try:
            # Dispatch task to the selected agent
            result = selected_agent_object.execute_task(task_payload)
            task["status"] = "completed"
            logging.info(f"Task '{task_id}' completed successfully. Result: {result}")
            return result
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            logging.error(f"Task '{task_id}' failed: {e}")
            # In a real system, this would trigger more sophisticated error handling
            return None
        finally:
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            if selected_agent_id:
                self.agent_manager.update_agent_load(selected_agent_id, -1) # Decrement agent load

    def _worker_loop(self):
        """
        The main loop for the worker thread that continuously processes tasks.
        Pops tasks based on priority from the heap.
        """
        while self.is_running:
            if self.task_queue:
                _priority, _task_id, task = heapq.heappop(self.task_queue) # Pop highest priority task
                self._execute_task(task)
            else:
                time.sleep(0.1)  # Wait a bit if no tasks are available

    def start(self):
        """
        Starts the automation engine's worker thread.
        """
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker_loop)
            self.worker_thread.start()
            # Start agent manager monitoring as well
            self.agent_manager.start_monitoring()
            logging.info("AutomationEngine started.")
        else:
            logging.info("AutomationEngine is already running.")

    def stop(self):
        """
        Stops the automation engine and waits for the worker thread to finish.
        """
        if self.is_running:
            logging.info("Stopping AutomationEngine...")
            self.is_running = False
            if self.worker_thread and self.worker_thread.is_alive():
                self.worker_thread.join()
            # Stop agent manager monitoring
            self.agent_manager.stop_monitoring()
            logging.info("AutomationEngine stopped.")
        else:
            logging.info("AutomationEngine is not running.")

    def get_task_status(self, task_id):
        """
        Retrieves the current status of a task.
        """
        # This is a simplified approach. In a real system, task status would be persisted.
        # Check running tasks first
        if task_id in self.running_tasks:
            return self.running_tasks[task_id]["status"]
        # Check queued tasks (in the heap)
        for _priority, _id, task in self.task_queue:
            if _id == task_id:
                return task["status"]
        return "not_found"

    def list_tasks(self):
        """
        Lists all tasks currently in the queue or running.
        """
        queued_tasks = [task["id"] for _priority, _id, task in self.task_queue]
        running_tasks = [t["id"] for t in self.running_tasks.values()]
        return {
            "queued": queued_tasks,
            "running": running_tasks
        }

    # Example Usage (for demonstration and testing)
if __name__ == "__main__":
    from src.agent.base_agent import BaseAgent

    class SampleAgent(BaseAgent):
        def __init__(self, agent_id, capabilities):
            super().__init__(agent_id, capabilities)

        def execute_task(self, task_payload):
            task_type = task_payload.get("type")
            if task_type == "sample_task":
                name = task_payload.get("name")
                duration = task_payload.get("duration")
                logging.info(f"Agent {self.agent_id}: Task '{name}' started. Will run for {duration} seconds.")
                time.sleep(duration)
                logging.info(f"Agent {self.agent_id}: Task '{name}' finished.")
                return f"Task {name} completed by {self.agent_id}"
            elif task_type == "quantum_encryption_task":
                algorithm = task_payload.get("algorithm")
                data = task_payload.get("data")
                logging.info(f"Agent {self.agent_id}: Performing quantum encryption with {algorithm} on data: {data[:10]}...")
                time.sleep(1) # Simulate encryption time
                logging.info(f"Agent {self.agent_id}: Quantum encryption with {algorithm} finished.")
                return f"Encrypted data with {algorithm} by {self.agent_id}"
            elif task_type == "error_task":
                raise ValueError("Simulated error for error_task")
            else:
                raise ValueError(f"Unknown task type: {task_type}")

    engine = AutomationEngine()
    engine.start()

    # Register agents with the engine's agent_manager
    pqc_agent_1 = SampleAgent("pqc_agent_001", ["sample_task", "quantum_encryption_task", "PQC_ENCRYPT_KYBER", "PQC_SIGN_DILITHIUM"])
    pqc_agent_2 = SampleAgent("pqc_agent_002", ["sample_task", "quantum_encryption_task", "PQC_ENCRYPT_KYBER"])
    kms_agent_1 = SampleAgent("kms_agent_001", ["KEY_ROTATION", "KEY_GENERATION"])

    engine.agent_manager.register_agent(pqc_agent_1.agent_id, pqc_agent_1, pqc_agent_1.capabilities)
    engine.agent_manager.register_agent(pqc_agent_2.agent_id, pqc_agent_2, pqc_agent_2.capabilities)
    engine.agent_manager.register_agent(kms_agent_1.agent_id, kms_agent_1, kms_agent_1.capabilities)

    # Add tasks with different priorities and required capabilities
    task1_id = engine.add_task("sample_task", {"name": "Task A", "duration": 2}, priority=5, required_capabilities=["sample_task"])
    task2_id = engine.add_task("quantum_encryption_task", {"algorithm": "Kyber", "data": "sensitive_data_1"}, priority=1, required_capabilities=["PQC_ENCRYPT_KYBER"])
    task3_id = engine.add_task("sample_task", {"name": "Task B", "duration": 1}, priority=10, required_capabilities=["sample_task"])
    task4_id = engine.add_task("quantum_encryption_task", {"algorithm": "Dilithium", "data": "sensitive_data_2"}, priority=3, required_capabilities=["PQC_SIGN_DILITHIUM"])
    error_task_id = engine.add_task("error_task", {"name": "Error Task"}, priority=2, required_capabilities=["sample_task"]) # This task will fail
    no_agent_task_id = engine.add_task("quantum_encryption_task", {"algorithm": "Falcon", "data": "data_3"}, priority=4, required_capabilities=["PQC_ENCRYPT_FALCON"]) # No suitable agent

    time.sleep(0.1) # Give some time for tasks to start processing

    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Kyber Encryption Task: {engine.get_task_status(task2_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task3_id)}")
    logging.info(f"Status of Dilithium Encryption Task: {engine.get_task_status(task4_id)}")
    logging.info(f"Status of Error Task: {engine.get_task_status(error_task_id)}")
    logging.info(f"Status of No Agent Task: {engine.get_task_status(no_agent_task_id)}")

    time.sleep(5) # Wait for tasks to potentially finish

    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Kyber Encryption Task: {engine.get_task_status(task2_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task3_id)}")
    logging.info(f"Status of Dilithium Encryption Task: {engine.get_task_status(task4_id)}")
    logging.info(f"Status of Error Task: {engine.get_task_status(error_task_id)}")
    logging.info(f"Status of No Agent Task: {engine.get_task_status(no_agent_task_id)}")

    logging.info(f"Current tasks: {engine.list_tasks()}")

    engine.stop()