import unittest
import os
import json
from src.feature_flagging import FeatureFlagManager

class TestFeatureFlagManager(unittest.TestCase):

    def setUp(self):
        self.config_file = 'test_feature_flags.json'
        # Ensure a clean state before each test
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        self.manager = FeatureFlagManager(config_file=self.config_file)

    def tearDown(self):
        # Clean up the config file after each test
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_initial_load_empty(self):
        self.assertEqual(self.manager.flags, {})

    def test_add_feature(self):
        self.manager.add_feature('new_feature', default_status=True)
        self.assertTrue(self.manager.is_feature_enabled('new_feature'))
        self.manager.add_feature('another_feature', default_status=False)
        self.assertFalse(self.manager.is_feature_enabled('another_feature'))

        # Verify it's saved to file
        with open(self.config_file, 'r') as f:
            flags_in_file = json.load(f)
        self.assertEqual(flags_in_file, {'new_feature': True, 'another_feature': False})

    def test_add_existing_feature(self):
        self.manager.add_feature('existing_feature', default_status=True)
        # Try to add again with different status, should not change
        self.manager.add_feature('existing_feature', default_status=False)
        self.assertTrue(self.manager.is_feature_enabled('existing_feature'))

    def test_set_feature_status(self):
        self.manager.add_feature('toggle_feature', default_status=False)
        self.assertFalse(self.manager.is_feature_enabled('toggle_feature'))

        self.manager.set_feature_status('toggle_feature', True)
        self.assertTrue(self.manager.is_feature_enabled('toggle_feature'))

        self.manager.set_feature_status('toggle_feature', False)
        self.assertFalse(self.manager.is_feature_enabled('toggle_feature'))

        # Verify it's saved to file
        with open(self.config_file, 'r') as f:
            flags_in_file = json.load(f)
        self.assertEqual(flags_in_file, {'toggle_feature': False})

    def test_set_feature_status_invalid_type(self):
        self.manager.add_feature('test_feature')
        with self.assertRaises(ValueError):
            self.manager.set_feature_status('test_feature', "invalid")

    def test_is_feature_enabled_non_existent(self):
        self.assertFalse(self.manager.is_feature_enabled('non_existent_feature'))

    def test_get_all_flags(self):
        self.manager.add_feature('feat1', True)
        self.manager.add_feature('feat2', False)
        all_flags = self.manager.get_all_flags()
        self.assertEqual(all_flags, {'feat1': True, 'feat2': False})
        # Ensure it returns a copy, not the internal dictionary
        all_flags['feat1'] = False
        self.assertTrue(self.manager.is_feature_enabled('feat1'))

    def test_remove_feature(self):
        self.manager.add_feature('to_be_removed', True)
        self.assertTrue(self.manager.is_feature_enabled('to_be_removed'))

        self.manager.remove_feature('to_be_removed')
        self.assertFalse(self.manager.is_feature_enabled('to_be_removed'))
        self.assertNotIn('to_be_removed', self.manager.flags)

        # Verify it's removed from file
        with open(self.config_file, 'r') as f:
            flags_in_file = json.load(f)
        self.assertEqual(flags_in_file, {})

    def test_remove_non_existent_feature(self):
        # Should not raise an error
        self.manager.remove_feature('non_existent_feature')
        self.assertEqual(self.manager.flags, {})

if __name__ == '__main__':
    unittest.main()