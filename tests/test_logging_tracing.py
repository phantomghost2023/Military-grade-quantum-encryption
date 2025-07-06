import unittest
import os
import json
from unittest.mock import patch, MagicMock
from src.logging_tracing import CentralizedLogger, DistributedTracer
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

class TestCentralizedLogger(unittest.TestCase):

    def setUp(self):
        self.log_file = 'test_app.log'
        self.logger = CentralizedLogger(log_file=self.log_file)

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_info_logging(self):
        message = "This is an info message."
        self.logger.info(message)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn("INFO", log_content)
        self.assertIn(message, log_content)

    def test_warning_logging(self):
        message = "This is a warning message."
        self.logger.warning(message)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn("WARNING", log_content)
        self.assertIn(message, log_content)

    def test_error_logging(self):
        message = "This is an error message."
        self.logger.error(message)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn("ERROR", log_content)
        self.assertIn(message, log_content)

    def test_critical_logging(self):
        message = "This is a critical message."
        self.logger.critical(message)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn("CRITICAL", log_content)
        self.assertIn(message, log_content)

    def test_debug_logging(self):
        message = "This is a debug message."
        self.logger.debug(message)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        self.assertIn("DEBUG", log_content)
        self.assertIn(message, log_content)

class TestDistributedTracer(unittest.TestCase):

    @patch('opentelemetry.sdk.trace.TracerProvider')
    @patch('opentelemetry.sdk.resources.Resource.create')
    @patch('opentelemetry.sdk.trace.export.SimpleSpanProcessor')
    @patch('opentelemetry.sdk.trace.export.ConsoleSpanExporter')
    def test_tracer_initialization(self, MockConsoleSpanExporter, MockSimpleSpanProcessor, MockResourceCreate, MockTracerProvider):
        service_name = "test-service"
        tracer = DistributedTracer(service_name)

        MockResourceCreate.assert_called_once_with({"service.name": service_name})
        MockTracerProvider.assert_called_once_with(resource=MockResourceCreate.return_value)
        MockSimpleSpanProcessor.assert_called_once_with(MockConsoleSpanExporter.return_value)
        MockTracerProvider.return_value.add_span_processor.assert_called_once_with(MockSimpleSpanProcessor.return_value)
        self.assertEqual(tracer.tracer, trace.get_tracer(service_name))

    @patch('opentelemetry.trace.get_tracer')
    def test_start_span(self, mock_get_tracer):
        mock_tracer_instance = MagicMock()
        mock_get_tracer.return_value = mock_tracer_instance

        tracer_obj = DistributedTracer("test-service")
        span_name = "test-span"
        attributes = {"key": "value"}

        with tracer_obj.start_span(span_name, attributes) as span:
            mock_tracer_instance.start_as_current_span.assert_called_once_with(span_name, attributes=attributes)
            self.assertEqual(span, mock_tracer_instance.start_as_current_span.return_value.__enter__.return_value)

if __name__ == '__main__':
    unittest.main()