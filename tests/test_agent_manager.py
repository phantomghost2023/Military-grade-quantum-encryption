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
        self.mock_agent_id = "test_agent_1"
        self.mock_capabilities = ["encryption", "decryption"]
        self.mock_agent = BaseAgent(self.mock_agent_id, self.mock_capabilities)

    def tearDown(self):
        # Ensure all agents are unregistered after each test
        for agent_id in list(self.agent_manager.agents.keys()):
            self.agent_manager.unregister_agent(agent_id)

    def test_register_agent(self):
        self.agent_manager.register_agent(self.mock_agent)
        self.assertIn(self.mock_agent_id, self.agent_manager.agents)
        self.assertEqual(self.agent_manager.agents[self.mock_agent_id].capabilities, self.mock_capabilities)

    def test_unregister_agent(self):
        self.agent_manager.register_agent(self.mock_agent)
        self.agent_manager.unregister_agent(self.mock_agent_id)
        self.assertNotIn(self.mock_agent_id, self.agent_manager.agents)

    def test_get_agent(self):
        self.agent_manager.register_agent(self.mock_agent)
        retrieved_agent = self.agent_manager.get_agent(self.mock_agent_id)
        self.assertIsNotNone(retrieved_agent)
        self.assertEqual(retrieved_agent.agent_id, self.mock_agent_id)

    def test_execute_agent_task(self):
        self.agent_manager.register_agent(self.mock_agent)
        mock_task_func = MagicMock(return_value="task_completed")
        self.agent_manager.execute_agent_task(self.mock_agent_id, mock_task_func, "arg1", kwarg="value1")
        mock_task_func.assert_called_once_with("arg1", kwarg="value1")

    def test_list_agents(self):
        self.agent_manager.register_agent(BaseAgent("agent_1", ["cap_a"]))
        self.agent_manager.register_agent(BaseAgent("agent_2", ["cap_b"]))
        agents = self.agent_manager.list_agents()
        self.assertEqual(len(agents), 2)
        self.assertIn("agent_1", [a.agent_id for a in agents])
        self.assertIn("agent_2", [a.agent_id for a in agents])

if __name__ == '__main__':
    unittest.main()