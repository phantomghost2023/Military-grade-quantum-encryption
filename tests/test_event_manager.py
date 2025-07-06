import unittest
from unittest.mock import MagicMock
from src.automation.event_manager import EventManager

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.mock_listener = MagicMock()

    def test_subscribe_and_publish(self):
        self.event_manager.subscribe('test_event', self.mock_listener)
        self.event_manager.publish('test_event', {'data': 'payload'})
        self.mock_listener.handle_event.assert_called_once_with('test_event', {'data': 'payload'})

    def test_unsubscribe(self):
        self.event_manager.subscribe('test_event', self.mock_listener)
        self.event_manager.unsubscribe('test_event', self.mock_listener)
        self.event_manager.publish('test_event', {'data': 'payload'})
        self.mock_listener.handle_event.assert_not_called()

    def test_publish_no_listeners(self):
        # Should not raise an error if no listeners are subscribed
        self.event_manager.publish('non_existent_event', {'data': 'payload'})

if __name__ == '__main__';
    unittest.main()