import random
import time

class ChaosEngineer:
    def __init__(self, automation_engine=None):
        self.automation_engine = automation_engine
        self.experiments = {
            "latency_injection": self._inject_latency,
            "error_injection": self._inject_error,
            "resource_exhaustion": self._exhaust_resources
        }

    def _inject_latency(self, task_id=None, min_delay_ms=100, max_delay_ms=1000):
        """Injects random latency into a task or a general operation."""
        delay = random.randint(min_delay_ms, max_delay_ms) / 1000.0
        print(f"[Chaos Engineering] Injecting {delay:.2f}s latency for task {task_id if task_id else 'general operation'}")
        time.sleep(delay)
        return True, f"Latency of {delay:.2f}s injected."

    def _inject_error(self, task_id=None, error_type="ValueError", message="Simulated error injection."):
        """Injects a simulated error into a task."""
        print(f"[Chaos Engineering] Injecting {error_type} for task {task_id if task_id else 'general operation'}")
        if error_type == "ValueError":
            raise ValueError(message)
        elif error_type == "RuntimeError":
            raise RuntimeError(message)
        elif error_type == "ConnectionError":
            raise ConnectionError(message)
        else:
            raise Exception(message)

    def _exhaust_resources(self, task_id=None, duration_s=5, cpu_load_percent=50):
        """Simulates resource exhaustion (e.g., high CPU usage)."""
        print(f"[Chaos Engineering] Simulating {cpu_load_percent}% CPU load for {duration_s}s for task {task_id if task_id else 'general operation'}")
        # This is a simplified simulation. Actual resource exhaustion requires more complex OS-level interaction.
        start_time = time.time()
        while time.time() - start_time < duration_s:
            # Simulate CPU work
            _ = [i*i for i in range(10000)]
            time.sleep(0.01 * (100 - cpu_load_percent) / 100) # Sleep to control load
        print(f"[Chaos Engineering] Resource exhaustion simulation complete for task {task_id if task_id else 'general operation'}")
        return True, "Resource exhaustion simulated."

    def run_experiment(self, experiment_name, **kwargs):
        """Runs a specified chaos engineering experiment."""
        if experiment_name in self.experiments:
            try:
                success, result_msg = self.experiments[experiment_name](**kwargs)
                return success, result_msg
            except Exception as e:
                return False, f"Experiment '{experiment_name}' failed: {e}"
        else:
            return False, f"Unknown experiment: {experiment_name}"

    def integrate_with_automation_engine(self, task_id, experiment_name, **kwargs):
        """Integrates chaos experiment with a specific task in the automation engine."""
        if self.automation_engine:
            print(f"[Chaos Engineering] Integrating experiment '{experiment_name}' with task '{task_id}'")
            # This is a conceptual integration. Actual integration would involve modifying task execution flow.
            # For example, wrapping task execution with experiment logic.
            try:
                success, msg = self.run_experiment(experiment_name, task_id=task_id, **kwargs)
                if not success:
                    print(f"[Chaos Engineering] Experiment failed for task {task_id}: {msg}")
                    # Optionally trigger self-healing or error handling
                    if self.automation_engine.error_handler:
                        self.automation_engine.error_handler.handle_error(f"Chaos experiment failed for task {task_id}: {msg}")
                return success, msg
            except Exception as e:
                print(f"[Chaos Engineering] Error during experiment integration for task {task_id}: {e}")
                return False, f"Error during experiment integration: {e}"
        else:
            return False, "Automation engine not provided for integration."

# Example Usage (for testing)
if __name__ == '__main__':
    # Dummy AutomationEngine for demonstration
    class DummyErrorHandler:
        def handle_error(self, error_msg):
            print(f"[Dummy Error Handler] Handling error: {error_msg}")

    class DummyAutomationEngine:
        def __init__(self):
            self.error_handler = DummyErrorHandler()

    dummy_engine = DummyAutomationEngine()
    chaos = ChaosEngineer(automation_engine=dummy_engine)

    print("\n--- Running Latency Injection Experiment ---")
    success, msg = chaos.run_experiment("latency_injection", min_delay_ms=50, max_delay_ms=200)
    print(f"Result: {success}, Message: {msg}")

    print("\n--- Running Error Injection Experiment (ValueError) ---")
    success, msg = chaos.run_experiment("error_injection", error_type="ValueError", message="Disk full simulation")
    print(f"Result: {success}, Message: {msg}")

    print("\n--- Running Resource Exhaustion Experiment ---")
    success, msg = chaos.run_experiment("resource_exhaustion", duration_s=2, cpu_load_percent=70)
    print(f"Result: {success}, Message: {msg}")

    print("\n--- Integrating Latency Injection with a Task ---")
    success, msg = chaos.integrate_with_automation_engine("task_123", "latency_injection", min_delay_ms=200, max_delay_ms=500)
    print(f"Result: {success}, Message: {msg}")

    print("\n--- Integrating Error Injection with a Task ---")
    success, msg = chaos.integrate_with_automation_engine("task_456", "error_injection", error_type="ConnectionError", message="DB connection lost")
    print(f"Result: {success}, Message: {msg}")