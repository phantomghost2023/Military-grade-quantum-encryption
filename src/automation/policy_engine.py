"""
policy_engine.py

This module defines the PolicyEngine for the automation system.
It allows for the definition and evaluation of policies to control automated tasks
and enforce permissions.
"""

class Policy:
    """
    Represents a single policy with a set of rules and associated actions.
    """
    def __init__(self, name: str, description: str, rules: dict, actions: list):
        self.name = name
        self.description = description
        self.rules = rules  # Rules defined as a dictionary (e.g., {"event_type": "key_expiration", "severity": "high"})
        self.actions = actions # Actions to take if rules are met (e.g., ["rotate_key", "notify_admin"])

    def __repr__(self):
        return f"Policy(name='{self.name}', description='{self.description}')"

class PolicyEngine:
    """
    The core policy evaluation engine.
    It loads policies and evaluates them against given contexts (events, requests).
    """
    def __init__(self):
        self.policies = [] # Stores loaded Policy objects

    def load_policy(self, policy: Policy):
        """
        Adds a policy to the engine.
        In a real system, policies would be loaded from a persistent store.
        """
        self.policies.append(policy)
        print(f"Policy '{policy.name}' loaded.")

    def evaluate(self, context: dict) -> list:
        """
        Evaluates all loaded policies against the given context.
        Returns a list of actions to be taken based on matching policies.

        Args:
            context (dict): A dictionary representing the current event or request
                            (e.g., {"event_type": "key_expiration", "severity": "high", "user_role": "admin"}).

        Returns:
            list: A list of actions prescribed by matching policies.
        """
        triggered_actions = []
        for policy in self.policies:
            if self._policy_matches(policy, context):
                print(f"Policy '{policy.name}' matched context.")
                triggered_actions.extend(policy.actions)
        return triggered_actions

    def _policy_matches(self, policy: Policy, context: dict) -> bool:
        """
        Checks if a policy's rules are satisfied by the given context.
        This is a simplified rule matching logic.
        """
        for rule_key, rule_value in policy.rules.items():
            if rule_key not in context or context[rule_key] != rule_value:
                return False
        return True

# Example Usage (for demonstration purposes)
if __name__ == "__main__":
    engine = PolicyEngine()

    # Define some example policies
    policy1 = Policy(
        name="High_Severity_Key_Expiration_Alert",
        description="Alerts admin on high severity key expiration.",
        rules={"event_type": "key_expiration", "severity": "high"},
        actions=["notify_admin", "log_critical_event"]
    )

    policy2 = Policy(
        name="Admin_Key_Rotation_Permission",
        description="Allows admin to rotate keys.",
        rules={"action_requested": "rotate_key", "user_role": "admin"},
        actions=["allow_action"]
    )

    engine.load_policy(policy1)
    engine.load_policy(policy2)

    # Simulate an event context
    event_context = {"event_type": "key_expiration", "severity": "high", "key_id": "KMS-001"}
    actions_for_event = engine.evaluate(event_context)
    print(f"Actions for event: {actions_for_event}")

    # Simulate a user request context
    request_context = {"action_requested": "rotate_key", "user_role": "admin", "key_id": "KMS-002"}
    actions_for_request = engine.evaluate(request_context)
    print(f"Actions for request: {actions_for_request}")

    unauthorized_request_context = {"action_requested": "rotate_key", "user_role": "guest", "key_id": "KMS-003"}
    actions_for_unauthorized_request = engine.evaluate(unauthorized_request_context)
    print(f"Actions for unauthorized request: {actions_for_unauthorized_request}")
