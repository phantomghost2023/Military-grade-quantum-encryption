"""
Module for comprehensive performance monitoring and profiling.
"""

import time
import functools

class PerformanceMonitor:
    """
    A class to provide utilities for performance monitoring and profiling.
    """

    def __init__(self):
        self.metrics = {}

    def measure_execution_time(self, func):
        """
        Decorator to measure the execution time of a function.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            self.metrics[func.__name__] = self.metrics.get(func.__name__, []) + [execution_time]
            print(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
            return result
        return wrapper

    def get_metrics(self):
        """
        Returns the collected performance metrics.
        """
        return self.metrics

    def reset_metrics(self):
        """
        Resets all collected performance metrics.
        """
        self.metrics = {}

# Example Usage (for demonstration, not part of the core library)
if __name__ == "__main__":
    monitor = PerformanceMonitor()

    @monitor.measure_execution_time
    def example_task(duration):
        time.sleep(duration)
        return "Task completed"

    example_task(0.1)
    example_task(0.2)

    print("\nCollected Metrics:", monitor.get_metrics())
    monitor.reset_metrics()
    print("Metrics after reset:", monitor.get_metrics())