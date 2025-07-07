import threading
import time
import logging
import threading
from collections import deque
from src.automation.ai_ml_integration import AIMLIntegration
from src.automation.self_healing import SelfHealing
from src.automation.performance_monitoring import PerformanceMonitor
from src.automation.chaos_engineering import ChaosEngineer
from src.disaster_recovery import DisasterRecovery
from src.policy_engine import Policy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomationEngine:
    """
    The core automation engine responsible for managing and executing tasks.
    It handles task scheduling, execution, and basic error handling.
    """
    def __init__(self,
                 ai_ml_integration: AIMLIntegration = None,
                 self_healing: SelfHealing = None,
                 performance_monitor: PerformanceMonitor = None,
                 chaos_engineer: ChaosEngineer = None,
                 disaster_recovery: DisasterRecovery = None,
                 policy_engine = None):
        self.task_queue = deque()  # Stores tasks to be executed
        self.running_tasks = {}  # Stores currently running tasks
        self.all_tasks = {} # Stores all tasks, including completed and failed
        self.task_id_counter = 0
        self.is_running = False
        self.worker_thread = None
        self.event_handlers = {} # For event-driven tasks
        self.policies = {} # Stores defined policies

        self.ai_ml_integration = ai_ml_integration if ai_ml_integration else AIMLIntegration()
        self.self_healing = self_healing if self_healing else SelfHealing(automation_engine=self)
        self.performance_monitor = performance_monitor if performance_monitor else PerformanceMonitor()
        self.chaos_engineer = chaos_engineer if chaos_engineer else ChaosEngineer(self)
        self.disaster_recovery = disaster_recovery if disaster_recovery else DisasterRecovery()
        self.policy_engine = policy_engine if policy_engine else PolicyEngine()
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
            "status": "queued",
            "result": None,
            "error": None
        }
        self.task_queue.append(task)
        self.all_tasks[task_id] = task # Store in all_tasks
        logging.info(f"Task '{task_id}' added to queue.")
        return task_id

    def _execute_task(self, task):
        """
        Executes a single task and updates its status.
        """
        task_id = task["id"]
        logging.info(f"Executing task '{task_id}'...")
        task["status"] = "running"
        task["start_time"] = time.time()
        self.running_tasks[task_id] = task

        try:
            result = task["function"](*task["args"], **task["kwargs"])
            task["status"] = "completed"
            task["result"] = result
            logging.info(f"Task '{task_id}' completed successfully. Result: {result}")
            return result
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            logging.error(f"Task '{task_id}' failed: {e}")
            # In a real system, this would trigger more sophisticated error handling
            return None
        finally:
            task["end_time"] = time.time()
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            # Basic error handling to trigger self-healing or AI/ML analysis
            if task["status"] == "failed":
                logging.error(f"Task '{task_id}' failed. Triggering self-healing/AI-ML analysis.")
                # Trigger self-healing for specific error types
                if "database_connection_failed" in task["error"].lower():
                    self.self_healing.check_and_heal({"type": "database_connection_failure", "details": task["error"]})
                # Log for AI/ML analysis for predictive maintenance
                self.ai_ml_integration.predict_maintenance_issue(task["error"])
                self.ai_ml_integration.resolve_error_intelligently(task["error"])
                # Evaluate policies for the failed task
                self.policy_engine.evaluate_policies({"event_type": "task_failure", "task_id": task_id, "error": task["error"]})

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
        task = self.all_tasks.get(task_id)
        if task:
            return task["status"]
        return "not_found"

    def get_all_tasks(self):
        """
        Returns a dictionary of all tasks managed by the engine.
        """
        return self.all_tasks

    def cancel_task(self, task_id):
        """
        Attempts to cancel a queued task.
        """
        task = self.all_tasks.get(task_id)
        if task and task["status"] == "queued":
            # Remove from queue if present
            for i, q_task in enumerate(self.task_queue):
                if q_task["id"] == task_id:
                    del self.task_queue[i]
                    break
            task["status"] = "cancelled"
            logging.info(f"Task '{task_id}' cancelled.")
            return True
        elif task and task["status"] == "running":
            logging.warning(f"Task '{task_id}' is running and cannot be cancelled.")
            return False
        logging.warning(f"Task '{task_id}' cannot be cancelled (not found or not queued).")
        return False

    def add_policy(self, policy_id, description, rules, actions):
        """
        Adds a new policy to the engine.
        """
        self.policies[policy_id] = {
            "policy_id": policy_id,
            "description": description,
            "rules": rules,
            "actions": actions
        }
        logging.info(f"Policy '{policy_id}' added.")

    def get_policies(self):
        """
        Retrieves all stored policies.
        """
        return list(self.policies.values())

    def register_event_handler(self, event_type: str, handler_function):
        """
        Registers a function to be called when a specific event occurs.
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler_function)
        logging.info(f"Handler '{handler_function.__name__}' registered for event '{event_type}'.")

    def emit_event(self, event_type: str, *args, **kwargs):
        """
        Emits an event, triggering all registered handlers for that event type.
        Handlers are executed as new tasks in the engine.
        """
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                self.add_task(handler, *args, **kwargs)
            logging.info(f"Event '{event_type}' emitted, {len(self.event_handlers[event_type])} handlers triggered.")
        else:
            logging.info(f"No handlers registered for event '{event_type}'.")

    def load_policy(self, policy: Policy):
        """
        Loads a policy into the engine's policy manager.
        """
        self.policy_engine.add_policy(policy.name, policy.rules, policy.actions)
        logging.info(f"Policy '{policy.name}' loaded into PolicyEngine.")

    def evaluate_policies(self, context: dict):
        """
        Evaluates policies based on the given context.
        """
        return self.policy_engine.evaluate_policies(context)

    def trigger_predictive_maintenance(self, data):
        """
        Triggers predictive maintenance analysis using the AI/ML integration.
        """
        return self.ai_ml_integration.predict_maintenance_issue(data)

    def trigger_intelligent_error_resolution(self, error_details):
        """
        Triggers intelligent error resolution using the AI/ML integration.
        """
        return self.ai_ml_integration.resolve_error_intelligently(error_details)

    def run_backup(self, data_sources, backup_name="manual_backup"):
        """
        Triggers a backup operation using the DisasterRecovery module.
        """
        logging.info(f"Initiating backup: {backup_name}")
        for source in data_sources:
            self.disaster_recovery.add_data_source(source)
        backup_path = self.disaster_recovery.create_backup(backup_name)
        if backup_path:
            logging.info(f"Backup '{backup_name}' created at: {backup_path}")
            return backup_path
        else:
            logging.error(f"Failed to create backup '{backup_name}'.")
            return None

    def run_restore(self, backup_name, restore_path):
        """
        Triggers a restore operation using the DisasterRecovery module.
        """
        logging.info(f"Initiating restore from backup: {backup_name} to {restore_path}")
        success = self.disaster_recovery.restore_backup(backup_name, restore_path)
        if success:
            logging.info(f"Restore from '{backup_name}' to '{restore_path}' completed successfully.")
        else:
            logging.error(f"Failed to restore from backup '{backup_name}'.")
        return success

    def list_backups(self):
        """
        Lists available backups.
        """
        return self.disaster_recovery.list_backups()

    def trigger_self_healing(self, issue_details):
        """
        Triggers self-healing actions based on detected issues.
        """
        self.self_healing.check_and_heal(issue_details)

    def register_event_task(self, event_type, task_function, *args, **kwargs):
        """
        Registers a task to be executed when a specific event occurs.
        """

    def execute_task_with_monitoring(self, task_name, task_func, *args, **kwargs):
        """
        Executes a task and measures its performance using the PerformanceMonitor.
        """
        logging.info(f"[AutomationEngine] Executing task '{task_name}' with performance monitoring...")
        # Apply the decorator to the task function dynamically
        monitored_task_func = self.performance_monitor.measure_execution_time(task_func)
        return monitored_task_func(*args, **kwargs)

    def get_performance_metrics(self):
        """
        Returns the performance metrics collected by the PerformanceMonitor.
        """
        return self.performance_monitor.get_metrics()

    def reset_performance_metrics(self):
        """
        Resets the performance metrics collected by the PerformanceMonitor.
        """
        self.performance_monitor.reset_metrics()
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append({
            "function": task_function,
            "args": args,
            "kwargs": kwargs
        })
        logging.info(f"Task registered for event '{event_type}'.")

    def run_chaos_experiment(self, experiment_name, **kwargs):
        """Runs a specified chaos engineering experiment."""
        return self.chaos_engineer.run_experiment(experiment_name, **kwargs)

    def integrate_chaos_with_task(self, task_id, experiment_name, **kwargs):
        """Integrates a chaos experiment with a specific task."""
        return self.chaos_engineer.integrate_with_automation_engine(task_id, experiment_name, **kwargs)

    def trigger_event_tasks(self, event_type, payload=None):
        """
        Triggers all registered tasks for a given event type.
        """
        logging.info(f"Event '{event_type}' triggered with payload: {payload}")
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                # Add event-triggered tasks to the main task queue
                self.add_task(handler["function"], *handler["args"], event_payload=payload, **handler["kwargs"])
        else:
            logging.info(f"No handlers registered for event '{event_type}'.")

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    def sample_task(name, duration, event_payload=None):
        logging.info(f"Task '{name}' started. Will run for {duration} seconds. Event Payload: {event_payload}")
        time.sleep(duration)
        logging.info(f"Task '{name}' finished.")
        return f"Task {name} completed"

    engine = AutomationEngine()
    engine.start()

    task1_id = engine.add_task(sample_task, "Task A", 2)
    task2_id = engine.add_task(sample_task, "Task B", 1)
    engine.add_task(lambda: 1/0, "Error Task", 0) # Task designed to fail

    time.sleep(0.5) # Give some time for tasks to start
    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task2_id)}")

    # Test event-driven tasks
    def event_triggered_task(payload):
        logging.info(f"Event-triggered task received payload: {payload}")

    engine.register_event_task("user_login", event_triggered_task)
    engine.trigger_event_tasks("user_login", {"username": "test_user", "timestamp": time.time()})

    time.sleep(3) # Wait for tasks to potentially finish

    logging.info(f"Status of Task A: {engine.get_task_status(task1_id)}")
    logging.info(f"Status of Task B: {engine.get_task_status(task2_id)}")
    logging.info(f"Status of Error Task: {engine.get_task_status('task_3')}")

    logging.info(f"Current tasks: {engine.list_tasks()}")
    logging.info(f"All tasks: {engine.get_all_tasks()}")

    # Test cancellation
    task4_id = engine.add_task(sample_task, "Task C", 10)
    logging.info(f"Status of Task C: {engine.get_task_status(task4_id)}")
    engine.cancel_task(task4_id)
    logging.info(f"Status of Task C after cancellation: {engine.get_task_status(task4_id)}")

    engine.stop()