import logging
from collections import defaultdict
import threading
import time
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EventManager:
    """
    Manages events and their corresponding handlers.
    Allows for event registration, emission, and asynchronous processing of events.
    """
    def __init__(self, automation_engine):
        self.handlers = defaultdict(list)  # event_type -> [handler_functions]
        self.event_queue = deque() # Stores events to be processed
        self.is_running = False
        self.worker_thread = None
        self.lock = threading.Lock() # To protect access to event_queue
        self.automation_engine = automation_engine # Store AutomationEngine instance
        logging.info("EventManager initialized.")

    def register_handler(self, event_type, handler_function):
        """
        Registers a handler function for a specific event type.
        """
        self.handlers[event_type].append(handler_function)
        logging.info(f"Handler '{handler_function.__name__}' registered for event type '{event_type}'.")

    def emit_event(self, event_type, payload=None):
        """
        Emits an event, adding it to the event queue for asynchronous processing.
        """
        event = {"type": event_type, "payload": payload, "timestamp": time.time()}
        with self.lock:
            self.event_queue.append(event)
        logging.info(f"Event '{event_type}' emitted with payload: {payload}.")

    def _process_events(self):
        """
        Worker loop to process events from the queue.
        """
        while self.is_running:
            event = None
            with self.lock:
                if self.event_queue:
                    event = self.event_queue.popleft()
            
            if event:
                event_type = event["type"]
                payload = event["payload"]
                logging.info(f"Processing event '{event_type}'...")
                # Trigger tasks registered in the AutomationEngine for this event type
                self.automation_engine.trigger_event_tasks(event_type, payload)

                if event_type in self.handlers:
                    for handler in self.handlers[event_type]:
                        try:
                            handler(payload) # Handlers receive the event payload
                            logging.info(f"Handler '{handler.__name__}' executed for event '{event_type}'.")
                        except Exception as e:
                            logging.error(f"Error executing handler '{handler.__name__}' for event '{event_type}': {e}")
                else:
                    logging.warning(f"No handlers registered for event type '{event_type}'.")
            else:
                time.sleep(0.05) # Small delay to prevent busy-waiting

    def start(self):
        """
        Starts the event manager's worker thread.
        """
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._process_events)
            self.worker_thread.start()
            logging.info("EventManager started.")
        else:
            logging.info("EventManager is already running.")

    def stop(self):
        """
        Stops the event manager and waits for the worker thread to finish.
        """
        if self.is_running:
            logging.info("Stopping EventManager...")
            self.is_running = False
            if self.worker_thread and self.worker_thread.is_alive():
                self.worker_thread.join()
            logging.info("EventManager stopped.")
        else:
            logging.info("EventManager is not running.")

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    from collections import deque # Import deque here for example usage

    def log_handler(event_data):
        logging.info(f"Log Handler received: {event_data}")

    def task_trigger_handler(task_info):
        logging.info(f"Task Trigger Handler received task: {task_info['name']}")
        # In a real system, this would interact with the AutomationEngine
        # For now, just simulate a task
        time.sleep(task_info.get('duration', 0.1))
        logging.info(f"Task '{task_info['name']}' simulated completion.")

    event_manager = EventManager()
    event_manager.start()

    # Register handlers
    event_manager.register_handler("system_log", log_handler)
    event_manager.register_handler("new_task", task_trigger_handler)
    event_manager.register_handler("user_login", log_handler)

    # Emit events
    print("\n--- Emitting Events ---")
    event_manager.emit_event("system_log", {"level": "INFO", "message": "System started successfully."})
    event_manager.emit_event("new_task", {"name": "DeployService", "priority": "high", "duration": 0.5})
    event_manager.emit_event("user_login", {"username": "alice", "ip": "192.168.1.100"})
    event_manager.emit_event("unknown_event", {"data": "This event has no registered handler."})

    time.sleep(1) # Give some time for events to be processed

    print("\n--- Stopping Event Manager ---")
    event_manager.stop()