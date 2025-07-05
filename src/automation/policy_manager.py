import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PolicyManager:
    """
    Manages policies and permissions for automation tasks.
    This class will define rules for task execution, user roles, and resource access.
    """
    def __init__(self):
        self.policies = {}
        self.roles = {}
        logging.info("PolicyManager initialized.")

    def add_policy(self, policy_name, rules):
        """
        Adds a new policy with a set of rules.
        Rules could be functions or data structures defining conditions.
        """
        if policy_name in self.policies:
            logging.warning(f"Policy '{policy_name}' already exists. Overwriting.")
        self.policies[policy_name] = rules
        logging.info(f"Policy '{policy_name}' added.")

    def get_policy(self, policy_name):
        """
        Retrieves a policy by its name.
        """
        return self.policies.get(policy_name)

    def delete_policy(self, policy_name):
        """
        Deletes a policy.
        """
        if policy_name in self.policies:
            del self.policies[policy_name]
            logging.info(f"Policy '{policy_name}' deleted.")
            return True
        logging.warning(f"Policy '{policy_name}' not found.")
        return False

    def add_role(self, role_name, permissions):
        """
        Adds a new role with associated permissions.
        Permissions could be a list of allowed actions or policy names.
        """
        if role_name in self.roles:
            logging.warning(f"Role '{role_name}' already exists. Overwriting.")
        self.roles[role_name] = permissions
        logging.info(f"Role '{role_name}' added with permissions: {permissions}.")

    def get_role_permissions(self, role_name):
        """
        Retrieves permissions for a given role.
        """
        return self.roles.get(role_name, [])

    def check_permission(self, user_roles, action, resource=None, policy_name=None, **kwargs):
        """
        Checks if any of the user's roles grant permission for a specific action on a resource,
        and optionally evaluates against a specific policy.
        """
        logging.info(f"Checking permission for roles {user_roles} to perform '{action}' on '{resource}' with policy '{policy_name}'.")

        # First, check role-based permissions
        for role in user_roles:
            permissions = self.get_role_permissions(role)
            if action in permissions or "*" in permissions:
                logging.debug(f"Role-based permission granted for role '{role}'.")
                # If a specific policy is requested, evaluate it
                if policy_name:
                    policy_rules = self.get_policy(policy_name)
                    if policy_rules:
                        if self._evaluate_policy(policy_rules, action, resource, **kwargs):
                            logging.info(f"Permission granted by role '{role}' and policy '{policy_name}'.")
                            return True
                        else:
                            logging.warning(f"Policy '{policy_name}' denied permission for action '{action}' on '{resource}'.")
                            return False
                    else:
                        logging.warning(f"Policy '{policy_name}' not found.")
                        return False # Deny if policy not found but specified
                else:
                    logging.info(f"Permission granted by role '{role}'. No specific policy required.")
                    return True
        
        logging.warning(f"Permission denied for roles {user_roles} to perform '{action}' on '{resource}'.")
        return False

    def _evaluate_policy(self, policy_rules, action, resource, **kwargs):
        """
        Evaluates a given set of policy rules against the action, resource, and additional kwargs.
        This method can be expanded to handle more complex rule structures.
        """
        # Example: A policy might have a list of allowed actions
        if "allowed_actions" in policy_rules:
            if action not in policy_rules["allowed_actions"] and "*" not in policy_rules["allowed_actions"] :
                return False
        
        # Example: A policy might restrict resources
        if "restricted_resources" in policy_rules:
            if resource in policy_rules["restricted_resources"]:
                return False

        # Example: Quantum-specific policy: enforce algorithm usage
        if action == "perform_quantum_encryption" and "allowed_algorithms" in policy_rules:
            requested_algorithm = kwargs.get("algorithm")
            if requested_algorithm not in policy_rules["allowed_algorithms"]:
                logging.warning(f"Quantum encryption denied: Algorithm '{requested_algorithm}' not allowed by policy.")
                return False
        
        # Add more complex policy evaluation logic here based on your needs
        # For now, if no specific denial rule is met, assume allowed by policy
        return True

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    policy_manager = PolicyManager()

    # Define some policies
    policy_manager.add_policy("admin_access", {"allow_all": True})
    policy_manager.add_policy("task_execution_policy", {"allowed_actions": ["sample_task", "deploy_app", "perform_quantum_encryption"]})
    policy_manager.add_policy("quantum_encryption_policy", {"allowed_algorithms": ["Kyber", "Dilithium"]})

    # Define roles and assign permissions
    policy_manager.add_role("admin", ["*"])
    policy_manager.add_role("developer", ["task_execution_policy", "view_logs"])
    policy_manager.add_role("quantum_engineer", ["perform_quantum_encryption"])
    policy_manager.add_role("guest", ["view_status"])

    # Test permissions
    print("\n--- Permission Checks ---")
    print(f"Admin can execute task: {policy_manager.check_permission(['admin'], 'execute_task')}")
    print(f"Developer can execute task: {policy_manager.check_permission(['developer'], 'execute_task', policy_name='task_execution_policy')}")
    print(f"Developer can view logs: {policy_manager.check_permission(['developer'], 'view_logs')}")
    print(f"Developer can delete policy: {policy_manager.check_permission(['developer'], 'delete_policy')}")
    print(f"Guest can view status: {policy_manager.check_permission(['guest'], 'view_status')}")
    print(f"Guest can execute task: {policy_manager.check_permission(['guest'], 'execute_task')}")

    # Test quantum-specific permissions
    print(f"Quantum Engineer can perform Kyber encryption: {policy_manager.check_permission(['quantum_engineer'], 'perform_quantum_encryption', algorithm='Kyber', policy_name='quantum_encryption_policy')}")
    print(f"Quantum Engineer can perform RSA encryption (should be denied): {policy_manager.check_permission(['quantum_engineer'], 'perform_quantum_encryption', algorithm='RSA', policy_name='quantum_encryption_policy')}")

    # Demonstrate policy retrieval and deletion
    print("\n--- Policy Management ---")
    print(f"Admin access policy: {policy_manager.get_policy('admin_access')}")
    policy_manager.delete_policy("admin_access")
    print(f"Admin access policy after deletion: {policy_manager.get_policy('admin_access')}")