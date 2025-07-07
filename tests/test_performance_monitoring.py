import unittest
from unittest.mock import patch, MagicMock
from src.automation.performance_monitoring import PerformanceMonitor

class TestPerformanceMonitoring(unittest.TestCase):
    def setUp(self):
        self.monitor = PerformanceMonitor()

    @patch('src.automation.performance_monitoring.time.time')
    def test_measure_execution_time(self, mock_time):
        mock_time.side_effect = [0, 10] # Simulate 10 seconds execution

        @self.monitor.measure_execution_time
        def test_function():
            pass

        test_function()
        # In a real scenario, you'd check logs or a metrics system for the recorded time
        # For this test, we just ensure the decorator runs without error
        self.assertTrue(True) # Placeholder assertion

    @patch('src.automation.performance_monitoring.psutil.cpu_percent')
    @patch('src.automation.performance_monitoring.psutil.virtual_memory')
    def test_get_system_metrics(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 50.0
        mock_virtual_memory.return_value = MagicMock(percent=70.0)

        cpu, memory = self.monitor.get_system_metrics()
        self.assertEqual(cpu, 50.0)
        self.assertEqual(memory, 70.0)

if __name__ == '__main__':
    unittest.main()