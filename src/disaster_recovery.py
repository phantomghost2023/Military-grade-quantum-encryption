import os
import shutil
import datetime
import zipfile

class DisasterRecovery:
    def __init__(self, backup_base_dir="./backups", data_to_backup=None):
        self.backup_base_dir = backup_base_dir
        self.data_to_backup = data_to_backup if data_to_backup is not None else []
        os.makedirs(self.backup_base_dir, exist_ok=True)

    def add_data_source(self, path, is_directory=False):
        if os.path.exists(path):
            self.data_to_backup.append({'path': path, 'is_directory': is_directory})
        else:
            print(f"Warning: Data source not found: {path}")

    def create_backup(self, backup_name=None):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup_name:
            backup_dir = os.path.join(self.backup_base_dir, f"{backup_name}_{timestamp}")
        else:
            backup_dir = os.path.join(self.backup_base_dir, f"backup_{timestamp}")
        
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Creating backup in: {backup_dir}")

        try:
            for item in self.data_to_backup:
                source_path = item['path']
                item_name = os.path.basename(source_path)
                destination_path = os.path.join(backup_dir, item_name)

                if item['is_directory']:
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(source_path, destination_path)
                print(f"Backed up: {source_path} to {destination_path}")
            
            # Create a zip archive of the backup directory
            zip_path = shutil.make_archive(backup_dir, 'zip', backup_dir)
            print(f"Backup successfully created at: {zip_path}")
            shutil.rmtree(backup_dir) # Remove the unzipped directory after zipping
            return zip_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            shutil.rmtree(backup_dir) # Clean up on error
            return None

    def restore_backup(self, backup_zip_path, restore_target_dir="./restored_data"):
        if not os.path.exists(backup_zip_path):
            print(f"Error: Backup zip file not found: {backup_zip_path}")
            return False

        os.makedirs(restore_target_dir, exist_ok=True)
        print(f"Restoring backup from {backup_zip_path} to {restore_target_dir}")

        try:
            with zipfile.ZipFile(backup_zip_path, 'r') as zip_ref:
                zip_ref.extractall(restore_target_dir)
            print("Backup restored successfully.")
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False

    def list_backups(self):
        backups = [f for f in os.listdir(self.backup_base_dir) if f.endswith('.zip')]
        return sorted(backups, reverse=True)

# Example Usage (for demonstration, not part of the file content)
# if __name__ == "__main__":
#     # Create some dummy data for backup
#     os.makedirs("test_data/configs", exist_ok=True)
#     with open("test_data/app_log.txt", "w") as f:
#         f.write("Log entry 1\nLog entry 2\n")
#     with open("test_data/configs/db_config.json", "w") as f:
#         f.write('{"host": "localhost", "port": 5432}')

#     dr = DisasterRecovery()
#     dr.add_data_source("test_data/app_log.txt")
#     dr.add_data_source("test_data/configs", is_directory=True)

#     # Create a backup
#     backup_file = dr.create_backup("my_application_data")

#     if backup_file:
#         print(f"Available backups: {dr.list_backups()}")

#         # Simulate data loss (optional)
#         # shutil.rmtree("test_data")

#         # Restore the backup
#         # dr.restore_backup(backup_file, "./restored_test_data")
#         # print("Data restored to ./restored_test_data")

#     # Clean up dummy data and backups
#     # shutil.rmtree("test_data", ignore_errors=True)
#     # shutil.rmtree("restored_test_data", ignore_errors=True)
#     # shutil.rmtree("backups", ignore_errors=True)