import unittest
from unittest.mock import patch, MagicMock
from src.automation.policy_manager import PolicyManager

class TestPolicyManager(unittest.TestCase):
    def setUp(self):
        self.policy_manager = PolicyManager()

    def test_get_policy(self):
        self.policy_manager.policies['test_policy'] = {'rules': []}
        policy = self.policy_manager.get_policy('test_policy')
        self.assertIsNotNone(policy)
        self.assertEqual(policy, {'rules': []})

    def test_get_non_existent_policy(self):
        self.assertIsNone(self.policy_manager.get_policy('non_existent_policy'))

    def test_add_policy(self):
        self.policy_manager.add_policy('test_policy', {'rule1': 'value1'})
        self.assertIn('test_policy', self.policy_manager.policies)
        self.assertEqual(self.policy_manager.policies['test_policy'], {'rule1': 'value1'})

    def test_delete_policy(self):
        self.policy_manager.add_policy('policy_to_delete', {'rule': 'value'})
        self.assertTrue(self.policy_manager.delete_policy('policy_to_delete'))
        self.assertNotIn('policy_to_delete', self.policy_manager.policies)

    def test_delete_non_existent_policy(self):
        self.assertFalse(self.policy_manager.delete_policy('non_existent_policy'))

    def test_add_role(self):
        self.policy_manager.add_role('admin_role', ['create', 'delete'])
        self.assertIn('admin_role', self.policy_manager.roles)
        self.assertEqual(self.policy_manager.roles['admin_role'], ['create', 'delete'])

    def test_get_role_permissions(self):
        self.policy_manager.add_role('user_role', ['view', 'edit'])
        permissions = self.policy_manager.get_role_permissions('user_role')
        self.assertEqual(permissions, ['view', 'edit'])

    def test_get_non_existent_role_permissions(self):
        permissions = self.policy_manager.get_role_permissions('non_existent_role')
        self.assertEqual(permissions, [])

    def test_check_permission_role_based_granted(self):
        self.policy_manager.add_role('admin', ['*'])
        self.assertTrue(self.policy_manager.check_permission(['admin'], 'any_action'))

    def test_check_permission_role_based_denied(self):
        self.policy_manager.add_role('user', ['view'])
        self.assertFalse(self.policy_manager.check_permission(['user'], 'delete'))

    def test_check_permission_with_policy_granted(self):
        self.policy_manager.add_role('dev', ['execute'])
        self.policy_manager.add_policy('exec_policy', {'allowed_actions': ['execute']})
        self.assertTrue(self.policy_manager.check_permission(['dev'], 'execute', policy_name='exec_policy'))

    def test_check_permission_with_policy_denied(self):
        self.policy_manager.add_role('dev', ['execute'])
        self.policy_manager.add_policy('exec_policy', {'allowed_actions': ['read']})
        self.assertFalse(self.policy_manager.check_permission(['dev'], 'execute', policy_name='exec_policy'))

    def test_check_permission_quantum_encryption_granted(self):
        self.policy_manager.add_role('quantum_engineer', ['perform_quantum_encryption'])
        self.policy_manager.add_policy('quantum_policy', {'allowed_algorithms': ['Kyber']})
        self.assertTrue(self.policy_manager.check_permission(['quantum_engineer'], 'perform_quantum_encryption', algorithm='Kyber', policy_name='quantum_policy'))

    def test_check_permission_quantum_encryption_denied(self):
        self.policy_manager.add_role('quantum_engineer', ['perform_quantum_encryption'])
        self.policy_manager.add_policy('quantum_policy', {'allowed_algorithms': ['Kyber']})
        self.assertFalse(self.policy_manager.check_permission(['quantum_engineer'], 'perform_quantum_encryption', algorithm='RSA', policy_name='quantum_policy'))

    def test_check_permission_policy_not_found(self):
        self.policy_manager.add_role('user', ['action'])
        self.assertFalse(self.policy_manager.check_permission(['user'], 'action', policy_name='non_existent_policy'))

if __name__ == '__main__':
    unittest.main()