import unittest
from unittest.mock import patch, MagicMock
from src.automation.chaos_engineering import ChaosEngineering

class TestChaosEngineering(unittest.TestCase):
    def setUp(self):
        self.chaos_engineer = ChaosEngineering()

    @patch('src.automation.chaos_engineering.random.choice')
    @patch('src.automation.chaos_engineering.ChaosEngineering._simulate_latency')
    @patch('src.automation.chaos_engineering.ChaosEngineering._simulate_resource_exhaustion')
    def test_inject_fault(self, mock_resource, mock_latency, mock_choice):
        mock_choice.return_value = 'latency'
        self.chaos_engineer.inject_fault()
        mock_latency.assert_called_once()
        mock_resource.assert_not_called()

        mock_choice.return_value = 'resource_exhaustion'
        self.chaos_engineer.inject_fault()
        mock_resource.assert_called_once()

    # Add more specific tests for _simulate_latency, _simulate_resource_exhaustion, etc.

if __name__ == '__main__';
    unittest.main()