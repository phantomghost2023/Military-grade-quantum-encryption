import threading
import time
import logging
from collections import deque

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
        self.task_id_counter = 0
        self.is_running = False
        self.worker_thread = None
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

        try:
            result = task["function"](*task["args"], **task["kwargs"])
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

    def _worker_loop(self):
        """
        The main loop for the worker thread that continuously processes tasks.
        """
        while self.is_running:
            if self.task_queue:
                task = self.task_queue.popleft()
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
        # This is a simplified approach. In a real system, task status would be persisted.
        for task in list(self.task_queue) + list(self.running_tasks.values()):
            if task["id"] == task_id:
                return task["status"]
        return "not_found"

    def list_tasks(self):
        """
        Lists all tasks currently in the queue or running.
        """
        return {
            "queued": [t["id"] for t in self.task_queue],
            "running": [t["id"] for t in self.running_tasks.values()]
        }

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    def sample_task(name, duration):
        logging.info(f"Task '{name}' started. Will run for {duration} seconds.")
        time.sleep(duration)
        logging.info(f"Task '{name}' finished.")
        return f"Task {name} completed"

    engine = AutomationEngine()
    engine.start()

    task1_id = engine.add_task(sample_task, "Task A", 2)
    task2_id = engine.add_task(sample_task, "Task B", 1)
    engine.add_task(lambda: 1/0, "Error Task") # Task designed to fail

    time.sleep(0.5) # Give some time for tasks to start
    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task2_id)}")

    time.sleep(3) # Wait for tasks to potentially finish

    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task2_id)}")
    logging.info(f"Status of Error Task: {engine.get_task_status('task_3')}")

    logging.info(f"Current tasks: {engine.list_tasks()}")

    engine.stop()