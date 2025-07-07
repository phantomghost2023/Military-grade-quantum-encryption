import unittest
from unittest.mock import MagicMock
from src.automation.event_manager import EventManager
import time

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.event_manager.start()
        self.mock_handler = MagicMock()

    def tearDown(self):
        self.event_manager.stop()

    def test_register_and_emit_event(self):
        self.event_manager.register_handler('test_event', self.mock_handler)
        self.event_manager.emit_event('test_event', {'data': 'test_payload'})
        time.sleep(0.1) # Give the worker thread some time to process the event
        self.mock_handler.assert_called_once_with({'data': 'test_payload'})

    def test_emit_event_no_handlers(self):
        # Emitting an event with no registered handlers should not raise an error
        self.event_manager.emit_event('unhandled_event', {'data': 'no_one_cares'})
        time.sleep(0.1)
        self.mock_handler.assert_not_called()

    def test_multiple_handlers(self):
        mock_handler_2 = MagicMock()
        self.event_manager.register_handler('multi_event', self.mock_handler)
        self.event_manager.register_handler('multi_event', mock_handler_2)
        self.event_manager.emit_event('multi_event', {'data': 'multiple_handlers'})
        time.sleep(0.1)
        self.mock_handler.assert_called_once_with({'data': 'multiple_handlers'})
        mock_handler_2.assert_called_once_with({'data': 'multiple_handlers'})

    def test_event_queue_processing(self):
        self.event_manager.register_handler('queue_event', self.mock_handler)
        for i in range(5):
            self.event_manager.emit_event('queue_event', {'order': i})
        time.sleep(0.5) # Give enough time for all events to be processed
        self.assertEqual(self.mock_handler.call_count, 5)
        # Verify the order of calls if necessary (mock_handler.call_args_list)

if __name__ == '__main__':
    unittest.main()