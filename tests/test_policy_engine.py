import unittest
from src.automation.policy_engine import PolicyEngine

class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.policy_engine = PolicyEngine()

    def test_add_and_evaluate_policy(self):
        # Example policy: allow if user is 'admin'
        self.policy_engine.add_policy('admin_access', lambda context: context.get('user') == 'admin')

        self.assertTrue(self.policy_engine.evaluate_policy('admin_access', {'user': 'admin'}))
        self.assertFalse(self.policy_engine.evaluate_policy('admin_access', {'user': 'guest'}))

    def test_evaluate_non_existent_policy(self):
        with self.assertRaises(ValueError):
            self.policy_engine.evaluate_policy('non_existent_policy', {})

    def test_remove_policy(self):
        self.policy_engine.add_policy('temp_policy', lambda context: True)
        self.assertTrue(self.policy_engine.remove_policy('temp_policy'))
        self.assertFalse(self.policy_engine.remove_policy('non_existent_policy'))

if __name__ == '__main__':
    unittest.main()