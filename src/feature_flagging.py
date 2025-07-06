import os
import json

class FeatureFlagManager:
    """Manages feature flags for the application."""

    def __init__(self, config_file='feature_flags.json'):
        self.config_file = config_file
        self.flags = self._load_flags()

    def _load_flags(self):
        """Loads feature flags from the configuration file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_flags(self):
        """Saves feature flags to the configuration file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.flags, f, indent=4)

    def is_feature_enabled(self, feature_name):
        """Checks if a specific feature is enabled."""
        return self.flags.get(feature_name, False)

    def set_feature_status(self, feature_name, enabled):
        """Sets the status of a feature flag."""
        if isinstance(enabled, bool):
            self.flags[feature_name] = enabled
            self._save_flags()
            print(f"Feature '{feature_name}' set to {'enabled' if enabled else 'disabled'}.")
        else:
            raise ValueError("Enabled status must be a boolean (True/False).")

    def get_all_flags(self):
        """Returns all feature flags and their statuses."""
        return self.flags.copy()

    def add_feature(self, feature_name, default_status=False):
        """Adds a new feature flag with a default status."""
        if feature_name not in self.flags:
            self.flags[feature_name] = default_status
            self._save_flags()
            print(f"Feature '{feature_name}' added with default status {'enabled' if default_status else 'disabled'}.")
        else:
            print(f"Feature '{feature_name}' already exists.")

    def remove_feature(self, feature_name):
        """Removes a feature flag."""
        if feature_name in self.flags:
            del self.flags[feature_name]
            self._save_flags()
            print(f"Feature '{feature_name}' removed.")
        else:
            print(f"Feature '{feature_name}' not found.")

if __name__ == '__main__':
    # Example Usage:
    flag_manager = FeatureFlagManager()

    # Add a new feature
    flag_manager.add_feature('new_dashboard', default_status=False)

    # Enable a feature
    flag_manager.set_feature_status('new_dashboard', True)

    # Check if a feature is enabled
    if flag_manager.is_feature_enabled('new_dashboard'):
        print("New dashboard feature is enabled!")
    else:
        print("New dashboard feature is disabled.")

    # Add another feature
    flag_manager.add_feature('experimental_kms', True)

    # Get all flags
    print("\nAll feature flags:", flag_manager.get_all_flags())

    # Disable a feature
    flag_manager.set_feature_status('experimental_kms', False)

    # Remove a feature
    flag_manager.remove_feature('new_dashboard')

    print("\nAll feature flags after removal:", flag_manager.get_all_flags())