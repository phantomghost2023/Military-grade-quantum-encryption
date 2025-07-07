import unittest
from src.automation.kms_automation_tasks import automated_key_rotation, automated_key_revocation, automated_key_generation
from src.kms_api import KMS
import os

class TestKMSAutomationTasks(unittest.TestCase):
    def setUp(self):
        # Ensure a clean key store for each test
        if os.path.exists("kms_key_store.json"):
            os.remove("kms_key_store.json")

    def tearDown(self):
        # Clean up after each test
        if os.path.exists("kms_key_store.json"):
            os.remove("kms_key_store.json")

    def test_automated_key_generation_and_rotation(self):
        # Test key generation
        gen_result = automated_key_generation("Kyber", "test_key_for_rotation")
        self.assertEqual(gen_result["status"], "success")
        self.assertEqual(gen_result["key_type"], "Kyber")
        self.assertEqual(gen_result["key_id"], "test_key_for_rotation")

        # Test key rotation
        rot_result = automated_key_rotation("test_key_for_rotation")
        self.assertEqual(rot_result["status"], "success")
        self.assertEqual(rot_result["key_id"], "test_key_for_rotation")
        self.assertIn("new_key_id", rot_result)

        # Verify old key is inactive and new key exists
        kms = KMS()
        old_key_info = kms.get_key("test_key_for_rotation")
        self.assertIsNotNone(old_key_info)
        self.assertEqual(old_key_info["status"], "inactive")

        new_key_info = kms.get_key(rot_result["new_key_id"])
        self.assertIsNotNone(new_key_info)
        self.assertEqual(new_key_info["status"], "active")

    def test_automated_key_revocation(self):
        # Generate a key to revoke
        gen_result = automated_key_generation("AES-256", "key_to_revoke")
        self.assertEqual(gen_result["status"], "success")

        # Test key revocation
        rev_result = automated_key_revocation("key_to_revoke")
        self.assertEqual(rev_result["status"], "success")
        self.assertEqual(rev_result["key_id"], "key_to_revoke")

        # Verify key is revoked
        kms = KMS()
        revoked_key_info = kms.get_key("key_to_revoke")
        self.assertIsNotNone(revoked_key_info)
        self.assertEqual(revoked_key_info["status"], "revoked")

    # Add more tests for other KMS automation tasks

if __name__ == '__main__':
    unittest.main()