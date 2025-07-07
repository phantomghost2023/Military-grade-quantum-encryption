import unittest
import time
import logging
import os
import sys
import queue
from unittest.mock import MagicMock, patch

# Add the project root to the sys.path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.automation.automation_engine import AutomationEngine
from src.automation.policy_engine import Policy, PolicyEngine
from src.automation.event_manager import EventManager
from src.automation.ai_ml_integration import AIMLIntegration
from src.automation.self_healing import SelfHealing
from src.performance_monitoring import PerformanceMonitor
from src.chaos_engineering import ChaosEngineer
from src.disaster_recovery import DisasterRecovery

# Suppress logging during tests for cleaner output
logging.disable(logging.CRITICAL)

class TestAutomationEngine(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_ai_ml_integration = MagicMock(spec=AIMLIntegration)
        self.mock_self_healing = MagicMock(spec=SelfHealing)
        self.mock_performance_monitor = MagicMock(spec=PerformanceMonitor)
        self.mock_chaos_engineer = MagicMock(spec=ChaosEngineer)
        self.mock_disaster_recovery = MagicMock(spec=DisasterRecovery)
        self.mock_policy_engine = MagicMock(spec=PolicyEngine)

        self.engine = AutomationEngine(
            ai_ml_integration=self.mock_ai_ml_integration,
            self_healing=self.mock_self_healing,
            performance_monitor=self.mock_performance_monitor,
            chaos_engineer=self.mock_chaos_engineer,
            disaster_recovery=self.mock_disaster_recovery,
            policy_engine=self.mock_policy_engine
        )
        self.engine.start()

    def tearDown(self):
        self.engine.stop()
        # Clear any remaining tasks in the queue and all_tasks dictionary
        while not self.engine.task_queue.empty():
            try:
                self.engine.task_queue.get_nowait()
            except queue.Empty:
                break
        self.engine.all_tasks.clear()
        # Ensure all worker threads are terminated
        for thread in self.engine.worker_threads:
            if thread.is_alive():
                thread.join(timeout=1) # Give a short timeout for the thread to finish

    def _wait_for_task_status(self, task_id, expected_status, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.engine.get_task_status(task_id)
            if status == expected_status:
                return True
            time.sleep(0.1) # Poll every 100ms
        self.fail(f"Task {task_id} did not reach status {expected_status} within {timeout} seconds. Current status: {status}")

    def test_add_task(self):
        def dummy_task(): pass
        task_id = self.engine.add_task(dummy_task)
        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.engine.all_tasks)
        self.assertEqual(self.engine.all_tasks[task_id]["status"], "queued")

    def test_task_execution_success(self):
        mock_function = MagicMock(return_value="success")
        task_id = self.engine.add_task(mock_function)
        self.assertTrue(self._wait_for_task_status(task_id, "completed", timeout=2)) # Give worker thread time to process
        self.assertEqual(self.engine.all_tasks[task_id]["status"], "completed")
        mock_function.assert_called_once()
        self.assertEqual(self.engine.all_tasks[task_id]["result"], "success")
        self.assertIsNotNone(self.engine.all_tasks[task_id]["start_time"])
        self.assertIsNotNone(self.engine.all_tasks[task_id]["end_time"])

    def test_task_execution_failure(self):
        mock_function = MagicMock(side_effect=ValueError("Simulated error"))
        task_id = self.engine.add_task(mock_function)
        self.assertTrue(self._wait_for_task_status(task_id, "failed", timeout=2))
        self.assertEqual(self.engine.all_tasks[task_id]["status"], "failed")
        mock_function.assert_called_once()
        self.assertIn("Simulated error", self.engine.all_tasks[task_id]["error"])
        self.assertIsNotNone(self.engine.all_tasks[task_id]["start_time"])
        self.assertIsNotNone(self.engine.all_tasks[task_id]["end_time"])
        self.engine.ai_ml_integration.predict_maintenance_issue.assert_called_once()
        self.engine.ai_ml_integration.resolve_error_intelligently.assert_called_once()

    def test_get_task_status(self):
        def dummy_task(): pass
        task_id = self.engine.add_task(dummy_task)
        self.assertEqual(self.engine.get_task_status(task_id), "queued")
        # Process the task to change its status
        mock_function = MagicMock(return_value="success")
        task_id_completed = self.engine.add_task(mock_function)
        self.assertTrue(self._wait_for_task_status(task_id_completed, "completed", timeout=2))
        self.assertEqual(self.engine.get_task_status(task_id_completed), "completed")
        self.assertIsNone(self.engine.get_task_status("non_existent_task"))

    def test_get_task_result(self):
        def task_with_result(): return 123
        task_id = self.engine.add_task(task_with_result)
        self.assertTrue(self._wait_for_task_status(task_id, "completed", timeout=2))
        self.assertEqual(self.engine.get_task_result(task_id), 123)
        self.assertIsNone(self.engine.get_task_result("non_existent_task"))

    def test_task_queue_processing_order(self):
        results = []
        def task_order(num):
            results.append(num)

        self.engine.add_task(task_order, 1)
        self.engine.add_task(task_order, 2)
        self.engine.add_task(task_order, 3)

        # Give time for all tasks to be processed
        time.sleep(0.5)
        self.assertEqual(results, [1, 2, 3])

    def test_get_task_result(self):
        def task_with_result(): return 123
        task_id = self.engine.add_task(task_with_result)
        self.assertTrue(self._wait_for_task_status(task_id, "completed", timeout=2))
        self.assertEqual(self.engine.get_task_result(task_id), 123)
        self.assertIsNone(self.engine.get_task_result("non_existent_task"))

    def test_task_queue_processing_order(self):
        results = []
        def task_order(num):
            results.append(num)

        self.engine.add_task(task_order, 1)
        self.engine.add_task(task_order, 2)
        self.engine.add_task(task_order, 3)

        # Give time for all tasks to be processed
        time.sleep(0.5)
        self.assertEqual(results, [1, 2, 3])

    def test_self_healing_trigger_on_failure(self):
        mock_function = MagicMock(side_effect=ValueError("database_connection_failed"))
        task_id = self.engine.add_task(mock_function)
        self.assertTrue(self._wait_for_task_status(task_id, "failed", timeout=2))
        self.mock_self_healing.check_and_heal.assert_called_once_with({"type": "database_connection_failure", "details": "database_connection_failed"})

    def test_ai_ml_integration_on_failure(self):
        mock_function = MagicMock(side_effect=ValueError("unforeseen_error"))
        task_id = self.engine.add_task(mock_function)
        self.assertTrue(self._wait_for_task_status(task_id, "failed", timeout=2))
        self.mock_ai_ml_integration.predict_maintenance_issue.assert_called_once_with("unforeseen_error")
        self.mock_ai_ml_integration.resolve_error_intelligently.assert_called_once_with("unforeseen_error")

    def test_event_driven_task_registration_and_emission(self):
        mock_handler = MagicMock()
        self.engine.register_event_handler("test_event", mock_handler)
        self.assertIn("test_event", self.engine.event_handlers)
        self.assertIn(mock_handler, self.engine.event_handlers["test_event"])

        self.engine.emit_event("test_event", "data1", key="value1")
        # Give time for event to be processed by the worker thread
        time.sleep(0.1)
        mock_handler.assert_called_once_with("data1", key="value1")

        self.engine.register_event_handler("task_failed", self.mock_self_healing.trigger_self_healing)
        self.engine.emit_event("task_failed", "test_task_id", "Test task failed.")
        self.mock_self_healing.trigger_self_healing.assert_called_once_with("test_task_id", "Test task failed.")

    def test_policy_evaluation_integration(self):
        # Test that policies are evaluated correctly
        mock_policy = MagicMock(spec=Policy)
        mock_policy.evaluate.return_value = True
        self.mock_policy_engine.evaluate_policies.return_value = [mock_policy]

        task_id = self.engine.add_task(lambda: False, "Test Policy Task")
        self.engine.start()
        self.engine.wait_for_task_completion(task_id)

        self.mock_policy_engine.evaluate_policies.assert_called_once_with("Test Policy Task", False)
        mock_policy.evaluate.assert_called_once_with("Test Policy Task", False)

class TestEventManager(unittest.TestCase):
    def setUp(self):
        # Mock AutomationEngine as EventManager now depends on it
        self.mock_automation_engine = MagicMock(spec=AutomationEngine)
        self.event_manager = EventManager(self.mock_automation_engine)
        self.event_manager.start()

    def tearDown(self):
        self.event_manager.stop()
        self.event_manager.event_queue.clear()

    def test_register_handler(self):
        mock_handler = MagicMock()
        mock_handler.__name__ = "mock_handler" # Assign a name for logging
        self.event_manager.register_handler("test_event", mock_handler)
        self.assertIn(mock_handler, self.event_manager.handlers["test_event"])

    def test_emit_event(self):
        mock_handler = MagicMock()
        mock_handler.__name__ = "mock_handler" # Assign a name for logging
        self.event_manager.register_handler("test_event", mock_handler)
        payload = {"key": "value"}
        self.event_manager.emit_event("test_event", payload)
        time.sleep(0.1) # Give worker thread time to process
        mock_handler.assert_called_once_with(payload)
        self.mock_automation_engine.trigger_event_tasks.assert_called_once_with("test_event", payload)

    def test_emit_event_no_handlers(self):
        payload = {"key": "value"}
        self.event_manager.emit_event("no_handler_event", payload)
        time.sleep(0.1) # Give worker thread time to process
        # Should not call any handler, but should still trigger automation engine
        self.mock_automation_engine.trigger_event_tasks.assert_called_once_with("no_handler_event", payload)

    def test_handler_exception_handling(self):
        def failing_handler(payload):
            raise ValueError("Handler Error")
        failing_handler.__name__ = "failing_handler" # Assign a name for logging
        mock_successful_handler = MagicMock()
        mock_successful_handler.__name__ = "mock_successful_handler" # Assign a name for logging
        self.event_manager.register_handler("error_event", failing_handler)
        self.event_manager.register_handler("error_event", mock_successful_handler)
        
        payload = {"data": "error"}
        self.event_manager.emit_event("error_event", payload)
        time.sleep(0.1) # Give worker thread time to process
        mock_successful_handler.assert_called_once_with(payload)
        # Check that the automation engine was still triggered despite handler error
        self.mock_automation_engine.trigger_event_tasks.assert_called_once_with("error_event", payload)

if __name__ == '__main__':
    unittest.main()
