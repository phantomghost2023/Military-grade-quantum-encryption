import unittest
from unittest.mock import patch, MagicMock
from src.automation.kms_automation_tasks import KMSAutomationTasks

class TestKMSAutomationTasks(unittest.TestCase):
    @patch('src.automation.kms_automation_tasks.KMSClient')
    def setUp(self, MockKMSClient):
        self.mock_kms_client = MockKMSClient.return_value
        self.kms_tasks = KMSAutomationTasks('http://mock-kms-url')

    def test_rotate_encryption_key(self):
        self.mock_kms_client.rotate_key.return_value = ('new_key_id', 'new_key_material')
        key_id, key_material = self.kms_tasks.rotate_encryption_key('old_key_id')
        self.assertEqual(key_id, 'new_key_id')
        self.assertEqual(key_material, 'new_key_material')
        self.mock_kms_client.rotate_key.assert_called_once_with('old_key_id')

    def test_audit_key_usage(self):
        self.mock_kms_client.audit_logs.return_value = ['log1', 'log2']
        logs = self.kms_tasks.audit_key_usage('key_id_to_audit')
        self.assertEqual(logs, ['log1', 'log2'])
        self.mock_kms_client.audit_logs.assert_called_once_with('key_id_to_audit')

    # Add more tests for other KMS automation tasks

if __name__ == '__main__';
    unittest.main()