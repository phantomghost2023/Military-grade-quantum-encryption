import unittest
from src.automation.agent_manager import AgentManager
from src.agent.base_agent import BaseAgent

class MockAgent(BaseAgent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.executed = False

    def execute(self, task):
        self.executed = True
        return f"Agent {self.agent_id} executed: {task}"

class TestAgentManager(unittest.TestCase):
    def setUp(self):
        self.agent_manager = AgentManager()
        self.mock_agent1 = MockAgent("agent1")
        self.mock_agent2 = MockAgent("agent2")

    def test_register_agent(self):
        self.agent_manager.register_agent(self.mock_agent1)
        self.assertIn("agent1", self.agent_manager.list_agents())

    def test_unregister_agent(self):
        self.agent_manager.register_agent(self.mock_agent1)
        self.agent_manager.unregister_agent("agent1")
        self.assertNotIn("agent1", self.agent_manager.list_agents())

    def test_get_agent(self):
        self.agent_manager.register_agent(self.mock_agent1)
        retrieved_agent = self.agent_manager.get_agent("agent1")
        self.assertEqual(retrieved_agent.agent_id, "agent1")

    def test_execute_agent_task(self):
        self.agent_manager.register_agent(self.mock_agent1)
        result = self.agent_manager.execute_agent_task("agent1", "perform_action")
        self.assertEqual(result, "Agent agent1 executed: perform_action")
        self.assertTrue(self.mock_agent1.executed)

    def test_list_agents(self):
        self.agent_manager.register_agent(self.mock_agent1)
        self.agent_manager.register_agent(self.mock_agent2)
        agents = self.agent_manager.list_agents()
        self.assertIn("agent1", agents)
        self.assertIn("agent2", agents)
        self.assertEqual(len(agents), 2)

if __name__ == '__main__';
    unittest.main()