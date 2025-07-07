import unittest
from unittest.mock import patch, MagicMock
from src.automation.orchestrator import Orchestrator

class TestOrchestrator(unittest.TestCase):
    @patch('src.automation.orchestrator.AgentManager')
    @patch('src.automation.orchestrator.EventManager')
    def setUp(self, MockEventManager, MockAgentManager):
        self.mock_agent_manager = MockAgentManager.return_value
        self.mock_event_manager = MockEventManager.return_value
        self.orchestrator = Orchestrator()

    def test_register_workflow(self):
        mock_workflow = MagicMock()
        self.orchestrator.register_workflow('test_workflow', mock_workflow)
        self.assertIn('test_workflow', self.orchestrator.workflows)

    def test_execute_workflow(self):
        mock_workflow = MagicMock()
        mock_workflow.execute.return_value = 'workflow_completed'
        self.orchestrator.register_workflow('test_workflow', mock_workflow)

        result = self.orchestrator.execute_workflow('test_workflow', {'param': 'value'})
        self.assertEqual(result, 'workflow_completed')
        mock_workflow.execute.assert_called_once_with({'param': 'value'})

    def test_execute_non_existent_workflow(self):
        with self.assertRaises(ValueError):
            self.orchestrator.execute_workflow('non_existent_workflow', {})

if __name__ == '__main__':
    unittest.main()