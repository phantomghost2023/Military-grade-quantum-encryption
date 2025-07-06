import unittest
import time
import logging
import os
import sys
from unittest.mock import MagicMock, patch

# Add the project root to the sys.path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.automation.automation_engine import AutomationEngine
from src.automation.policy_engine import Policy, PolicyEngine
from src.automation.event_manager import EventManager

# Suppress logging during tests for cleaner output
logging.disable(logging.CRITICAL)

class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()

    def test_policy_creation(self):
        policy = Policy("test_policy", "A test policy", {"key": "value"}, ["action1"])
        self.assertEqual(policy.name, "test_policy")
        self.assertEqual(policy.rules, {"key": "value"})
        self.assertEqual(policy.actions, ["action1"])

    def test_load_policy(self):
        policy = Policy("test_policy", "A test policy", {"key": "value"}, ["action1"])
        self.engine.load_policy(policy)
        self.assertIn(policy, self.engine.policies)

    def test_evaluate_matching_policy(self):
        policy = Policy("allow_access", "Allow access", {"user": "admin"}, ["grant_access"])
        self.engine.load_policy(policy)
        context = {"user": "admin", "resource": "data"}
        actions = self.engine.evaluate(context)
        self.assertIn("grant_access", actions)

    def test_evaluate_non_matching_policy(self):
        policy = Policy("deny_access", "Deny access", {"user": "guest"}, ["deny_access"])
        self.engine.load_policy(policy)
        context = {"user": "admin", "resource": "data"}
        actions = self.engine.evaluate(context)
        self.assertNotIn("deny_access", actions)

    def test_evaluate_multiple_policies(self):
        policy1 = Policy("policy1", "Desc1", {"type": "A"}, ["action_A"])
        policy2 = Policy("policy2", "Desc2", {"type": "B"}, ["action_B"])
        policy3 = Policy("policy3", "Desc3", {"type": "A", "status": "active"}, ["action_C"])
        self.engine.load_policy(policy1)
        self.engine.load_policy(policy2)
        self.engine.load_policy(policy3)

        context = {"type": "A", "status": "active", "user": "test"}
        actions = self.engine.evaluate(context)
        self.assertIn("action_A", actions)
        self.assertIn("action_C", actions)
        self.assertNotIn("action_B", actions)

class TestAutomationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AutomationEngine()
        self.engine.start() # Start the worker thread

    def tearDown(self):
        self.engine.stop() # Stop the worker thread
        # Clean up any remaining tasks in the queue for subsequent tests
        self.engine.task_queue.clear()
        self.engine.running_tasks.clear()
        self.engine.all_tasks.clear()

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
        def failing_task(): raise ValueError("Test Error")
        task_id = self.engine.add_task(failing_task)
        time.sleep(0.1) # Give worker thread time to process
        self.assertEqual(self.engine.all_tasks[task_id]["status"], "failed")
        self.assertIn("Test Error", self.engine.all_tasks[task_id]["error"])
        self.assertIsNotNone(self.engine.all_tasks[task_id]["start_time"])
        self.assertIsNotNone(self.engine.all_tasks[task_id]["end_time"])

    def test_get_task_status(self):
        def long_task(): time.sleep(0.5)
        task_id = self.engine.add_task(long_task)
        self.assertEqual(self.engine.get_task_status(task_id), "queued")
        self.assertTrue(self._wait_for_task_status(task_id, "running", timeout=2)) # Increased timeout
        self.assertEqual(self.engine.get_task_status(task_id), "running") # Should still be running
        self.assertTrue(self._wait_for_task_status(task_id, "completed", timeout=2)) # Increased timeout
        self.assertEqual(self.engine.get_task_status("non_existent_task"), "not_found")

    def test_cancel_task(self):
        def never_run_task(): pass
        task_id = self.engine.add_task(never_run_task)
        self.assertTrue(self.engine.cancel_task(task_id))
        self.assertEqual(self.engine.all_tasks[task_id]["status"], "cancelled")
        self.assertNotIn(task_id, [t["id"] for t in self.engine.task_queue])

    def test_cancel_running_task_fails(self):
        def long_task(): time.sleep(1)
        task_id = self.engine.add_task(long_task)
        time.sleep(0.5) # Let it start running
        self.assertFalse(self.engine.cancel_task(task_id))
        self.assertEqual(self.engine.all_tasks[task_id]["status"], "running")

    def test_get_all_tasks(self):
        def task1(): pass
        def task2(): pass
        self.engine.add_task(task1)
        self.engine.add_task(task2)
        all_tasks = self.engine.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)
        self.assertIn("task_1", all_tasks)
        self.assertIn("task_2", all_tasks)

    def test_add_policy_and_get_policies(self):
        self.engine.add_policy("test_policy", "desc", {"rule": "val"}, ["action"])
        policies = self.engine.get_policies()
        self.assertEqual(len(policies), 1)
        self.assertEqual(policies[0]["policy_id"], "test_policy")

    def test_register_and_trigger_event_task(self):
        mock_event_task = MagicMock()
        self.engine.register_event_task("test_event", mock_event_task, arg1="arg1", kwarg1="val1")
        
        event_payload = {"data": "some_data"}
        self.engine.trigger_event_tasks("test_event", event_payload)
        
        time.sleep(0.1) # Give worker thread time to process
        mock_event_task.assert_called_once_with(event_payload=event_payload, arg1="arg1", kwarg1="val1")

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
