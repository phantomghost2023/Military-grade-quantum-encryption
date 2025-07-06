import unittest
from unittest.mock import patch, MagicMock
from src.automation.policy_manager import PolicyManager

class TestPolicyManager(unittest.TestCase):
    def setUp(self):
        self.policy_manager = PolicyManager()

    def test_load_policies_from_file(self):
        # Create a mock policy file
        mock_policy_content = """
policies:
  - name: test_policy_1
    rules:
      - type: allow
        condition: user == 'admin'
  - name: test_policy_2
    rules:
      - type: deny
        condition: ip == '192.168.1.1'
"""
        with patch('builtins.open', unittest.mock.mock_open(read_data=mock_policy_content)) as mock_file:
            with patch('src.automation.policy_manager.yaml.safe_load') as mock_yaml_load:
                mock_yaml_load.return_value = {
                    'policies': [
                        {'name': 'test_policy_1', 'rules': [{'type': 'allow', 'condition': 'user == \'admin\''}]},
                        {'name': 'test_policy_2', 'rules': [{'type': 'deny', 'condition': 'ip == \'192.168.1.1\''}]}
                    ]
                }
                self.policy_manager.load_policies('mock_policies.yaml')
                self.assertIn('test_policy_1', self.policy_manager.policies)
                self.assertIn('test_policy_2', self.policy_manager.policies)

    def test_get_policy(self):
        self.policy_manager.policies['test_policy'] = {'rules': []}
        policy = self.policy_manager.get_policy('test_policy')
        self.assertIsNotNone(policy)
        self.assertEqual(policy, {'rules': []})

    def test_get_non_existent_policy(self):
        self.assertIsNone(self.policy_manager.get_policy('non_existent_policy'))

if __name__ == '__main__';
    unittest.main()