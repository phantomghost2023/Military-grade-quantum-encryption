import unittest
from src.automation.api_interface import app

class TestAutomationAPIInterface(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_task_workflow(self):
        # Test task creation
        response = self.app.post(
            '/api/v1/tasks',
            json={'task_function_name': 'test_workflow', 'args': [{'param': 'value'}]}
        )
        self.assertEqual(response.status_code, 202)
        self.assertIn('task_id', response.json)
        task_id = response.json['task_id']

        # Test getting task status
        response = self.app.get(f'/api/v1/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json)

    # Add more tests for other API methods

if __name__ == '__main__':
    unittest.main()