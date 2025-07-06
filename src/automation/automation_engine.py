import threading
import time
import logging
from collections import deque
from src.automation.policy_engine import PolicyEngine, Policy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomationEngine:
    """
    The core automation engine responsible for managing and executing tasks.
    It handles task scheduling, execution, and basic error handling.
    """
    def __init__(self):
        self.task_queue = deque()  # Stores tasks to be executed
        self.running_tasks = {}  # Stores currently running tasks
        self.all_tasks = {} # New: Stores all tasks, including completed and failed
        self.task_id_counter = 0
        self.is_running = False
        self.worker_thread = None
        self.policy_engine = PolicyEngine()
        self.event_task_mappings = {} # New: Stores mappings from event_type to task_function
        logging.info("AutomationEngine initialized.")

    def _generate_task_id(self):
        self.task_id_counter += 1
        return f"task_{self.task_id_counter}"

    def add_task(self, task_function, *args, **kwargs):
        """
        Adds a new task to the automation engine's queue.
        A task is a callable function along with its arguments.
        """
        task_id = self._generate_task_id()
        task = {
            "id": task_id,
            "function": task_function,
            "args": args,
            "kwargs": kwargs,
            "status": "queued"
        }
        self.task_queue.append(task)
        self.all_tasks[task_id] = task # Add to all_tasks
        logging.info(f"Task '{task_id}' added to queue.")
        return task_id

    def _execute_task(self, task):
        """
        Executes a single task and updates its status.
        """
        task_id = task["id"]
        logging.info(f"Executing task '{task_id}'...")
        task["status"] = "running"
        self.running_tasks[task_id] = task

        task["start_time"] = time.time() # Record start time

        try:
            result = task["function"](*task["args"], **task["kwargs"])
            task["status"] = "completed"
            task["result"] = result # Record result
            logging.info(f"Task '{task_id}' completed successfully. Result: {result}")
            return result
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            logging.error(f"Task '{task_id}' failed: {e}")
            # In a real system, this would trigger more sophisticated error handling
            return None
        finally:
            task["end_time"] = time.time() # Record end time
            # Task is no longer running, but remains in all_tasks for history
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]

    def _worker_loop(self):
        """
        The main loop for the worker thread that continuously processes tasks.
        """
        while self.is_running:
            if self.task_queue:
                task = self.task_queue.popleft()
                self._execute_task(task)
            else:
                time.sleep(0.01)  # Wait a bit if no tasks are available

    def start(self):
        """
        Starts the automation engine's worker thread.
        """
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker_loop)
            self.worker_thread.start()
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
            logging.info("AutomationEngine stopped.")
        else:
            logging.info("AutomationEngine is not running.")

    def get_task_status(self, task_id):
        """
        Retrieves the current status of a task.
        """
        task = self.all_tasks.get(task_id)
        if task:
            return task["status"]
        return "not_found"

    def register_event_task(self, event_type: str, task_function, *args, **kwargs):
        """
        Registers a task function to be executed when a specific event type is emitted.
        The task_function will be added to the engine's queue when the event occurs.
        """
        if event_type not in self.event_task_mappings:
            self.event_task_mappings[event_type] = []
        self.event_task_mappings[event_type].append({
            "function": task_function,
            "args": args,
            "kwargs": kwargs
        })
        logging.info(f"Registered task for event type: {event_type}")

    def trigger_event_tasks(self, event_type: str, event_payload: dict = None):
        """
        Triggers all tasks registered for a given event type.
        """
        if event_type in self.event_task_mappings:
            logging.info(f"Triggering tasks for event type: {event_type}")
            for mapping in self.event_task_mappings[event_type]:
                # Pass event_payload as the first argument to the task function
                # if the task function expects it.
                task_args = (event_payload,) + mapping["args"]
                self.add_task(mapping["function"], *task_args, **mapping["kwargs"])
        else:
            logging.info(f"No tasks registered for event type: {event_type}")

    def add_policy(self, name: str, description: str, rules: dict, actions: list):
        """
        Adds a new policy to the policy engine.
        """
        new_policy = Policy(name, description, rules, actions)
        self.policy_engine.load_policy(new_policy)
        return new_policy.name

    def get_policies(self):
        """
        Retrieves all loaded policies.
        """
        return [policy.__dict__ for policy in self.policy_engine.policies]

    def get_policy(self, policy_name: str):
        """
        Retrieves a specific policy by name.
        """
        for policy in self.policy_engine.policies:
            if policy.name == policy_name:
                return policy.__dict__
        return None

    def update_policy(self, policy_name: str, new_description: str = None, new_rules: dict = None, new_actions: list = None):
        """
        Updates an existing policy.
        """
        for policy in self.policy_engine.policies:
            if policy.name == policy_name:
                if new_description is not None:
                    policy.description = new_description
                if new_rules is not None:
                    policy.rules = new_rules
                if new_actions is not None:
                    policy.actions = new_actions
                logging.info(f"Policy '{policy_name}' updated.")
                return True
        return False

    def delete_policy(self, policy_name: str):
        """
        Deletes a policy by name.
        """
        initial_len = len(self.policy_engine.policies)
        self.policy_engine.policies = [p for p in self.policy_engine.policies if p.name != policy_name]
        if len(self.policy_engine.policies) < initial_len:
            logging.info(f"Policy '{policy_name}' deleted.")
            return True
        return False

    def list_tasks(self):
        """
        Lists all tasks currently in the queue or running.
        """
        return {
            "queued": [t["id"] for t in self.task_queue],
            "running": [t["id"] for t in self.running_tasks.values()]
        }

    def get_all_tasks(self):
        """
        Retrieves all tasks, including queued, running, completed, and failed.
        """
        # Return a copy to prevent external modification
        return {task_id: {k: v for k, v in task.items() if k != 'function'} for task_id, task in self.all_tasks.items()}

    def cancel_task(self, task_id: str):
        """
        Cancels a queued task.
        """
        for i, task in enumerate(self.task_queue):
            if task["id"] == task_id:
                del self.task_queue[i]
                self.all_tasks[task_id]["status"] = "cancelled"
                logging.info(f"Task '{task_id}' cancelled.")
                return True
        logging.warning(f"Task '{task_id}' not found in queue or already running/completed.")
        return False

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    from src.automation.policy_engine import Policy # Import Policy for example usage

    def sample_task(name, duration):
        logging.info(f"Task '{name}' started. Will run for {duration} seconds.")
        time.sleep(duration)
        logging.info(f"Task '{name}' finished.")
        return f"Task {name} completed"

    engine = AutomationEngine()
    engine.start()

    task1_id = engine.add_task(sample_task, "Task A", 2)
    task2_id = engine.add_task(sample_task, "Task B", 1)
    task3_id = engine.add_task(lambda: 1/0, "Error Task") # Task designed to fail

    logging.info(f"All tasks: {engine.get_all_tasks()}")

    time.sleep(0.5) # Give some time for tasks to start
    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task2_id)}")

    engine.cancel_task(task1_id) # Try to cancel a running task (should fail)
    engine.cancel_task(task3_id) # Try to cancel a queued task (should succeed)

    time.sleep(3) # Wait for tasks to potentially finish

    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task2_id)}")
    logging.info(f"Status of Error Task: {engine.get_task_status(task3_id)}")

    logging.info(f"Current tasks: {engine.list_tasks()}")
    logging.info(f"All tasks after completion: {engine.get_all_tasks()}")

    engine.stop()