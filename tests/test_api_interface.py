import unittest
from unittest.mock import patch, MagicMock
from src.automation.api_interface import AutomationAPIInterface

class TestAutomationAPIInterface(unittest.TestCase):
    def setUp(self):
        self.api_interface = AutomationAPIInterface()

    @patch('src.automation.api_interface.requests.post')
    def test_trigger_automation(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'success', 'task_id': '123'}
        mock_post.return_value.status_code = 200

        response = self.api_interface.trigger_automation('test_workflow', {'param': 'value'})
        self.assertEqual(response, {'status': 'success', 'task_id': '123'})
        mock_post.assert_called_once_with(
            'http://localhost:8000/api/automation/trigger',
            json={'workflow_name': 'test_workflow', 'parameters': {'param': 'value'}}
        )

    @patch('src.automation.api_interface.requests.get')
    def test_get_automation_status(self, mock_get):
        mock_get.return_value.json.return_value = {'status': 'completed'}
        mock_get.return_value.status_code = 200

        response = self.api_interface.get_automation_status('123')
        self.assertEqual(response, {'status': 'completed'})
        mock_get.assert_called_once_with('http://localhost:8000/api/automation/status/123')

    # Add more tests for other API methods

if __name__ == '__main__';
    unittest.main()