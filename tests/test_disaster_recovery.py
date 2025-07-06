import unittest
import os
import shutil
import zipfile
from datetime import datetime
from src.disaster_recovery import DisasterRecovery

class TestDisasterRecovery(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_dr_data'
        self.backup_dir = 'test_backups'
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        # Create some dummy data files
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write('content of file1')
        with open(os.path.join(self.test_dir, 'file2.txt'), 'w') as f:
            f.write('content of file2')
        os.makedirs(os.path.join(self.test_dir, 'subdir'), exist_ok=True)
        with open(os.path.join(self.test_dir, 'subdir', 'file3.txt'), 'w') as f:
            f.write('content of file3')

        self.dr = DisasterRecovery(backup_base_path=self.backup_dir)
        self.dr.add_data_source(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)

    def test_add_data_source(self):
        self.assertIn(self.test_dir, self.dr.data_sources)

    def test_create_backup(self):
        backup_path = self.dr.create_backup()
        self.assertTrue(os.path.exists(backup_path))
        self.assertTrue(zipfile.is_zipfile(backup_path))

        # Verify contents of the backup
        with zipfile.ZipFile(backup_path, 'r') as zf:
            namelist = zf.namelist()
            self.assertIn(os.path.join(os.path.basename(self.test_dir), 'file1.txt').replace('\\', '/'), namelist)
            self.assertIn(os.path.join(os.path.basename(self.test_dir), 'file2.txt').replace('\\', '/'), namelist)
            self.assertIn(os.path.join(os.path.basename(self.test_dir), 'subdir', 'file3.txt').replace('\\', '/'), namelist)

    def test_list_backups(self):
        # Create a few backups
        self.dr.create_backup()
        self.dr.create_backup()
        backups = self.dr.list_backups()
        self.assertEqual(len(backups), 2)
        for backup in backups:
            self.assertTrue(backup.startswith(os.path.join(self.backup_dir, 'backup_').replace('\\', '/')))
            self.assertTrue(backup.endswith('.zip'))

    def test_restore_backup(self):
        backup_path = self.dr.create_backup()
        
        # Remove original data to simulate disaster
        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)

        restore_target = 'test_restore_target'
        os.makedirs(restore_target, exist_ok=True)

        self.dr.restore_backup(backup_path, restore_target)

        # Verify restored files
        self.assertTrue(os.path.exists(os.path.join(restore_target, os.path.basename(self.test_dir), 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(restore_target, os.path.basename(self.test_dir), 'file2.txt')))
        self.assertTrue(os.path.exists(os.path.join(restore_target, os.path.basename(self.test_dir), 'subdir', 'file3.txt')))

        with open(os.path.join(restore_target, os.path.basename(self.test_dir), 'file1.txt'), 'r') as f:
            self.assertEqual(f.read(), 'content of file1')

        shutil.rmtree(restore_target)

    def test_restore_backup_non_existent(self):
        with self.assertRaises(FileNotFoundError):
            self.dr.restore_backup('non_existent_backup.zip', 'restore_target')

if __name__ == '__main__':
    unittest.main()