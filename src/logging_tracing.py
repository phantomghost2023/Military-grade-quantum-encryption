import logging
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

class DistributedTracer:
    def __init__(self, service_name="quantum-encryption-service"):
        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        # Export spans to console for demonstration
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        # For production, export to an OTLP collector (e.g., Jaeger, Zipkin)
        # provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(__name__)

    def start_span(self, span_name, parent_span=None):
        if parent_span:
            return self.tracer.start_as_current_span(span_name, context=trace.set_span_in_context(parent_span))
        else:
            return self.tracer.start_as_current_span(span_name)

class CentralizedLogger:
    def __init__(self, name="quantum-encryption-logger", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, message, **kwargs):
        self.logger.info(message, extra=kwargs)

    def warning(self, message, **kwargs):
        self.logger.warning(message, extra=kwargs)

    def error(self, message, **kwargs):
        self.logger.error(message, extra=kwargs)

    def debug(self, message, **kwargs):
        self.logger.debug(message, extra=kwargs)

# Example Usage (for demonstration, not part of the file content)
# if __name__ == "__main__":
#     logger = CentralizedLogger()
#     tracer = DistributedTracer()

#     with tracer.start_span("main-operation") as parent_span:
#         logger.info("Starting main operation.", operation_id="op123")

#         with tracer.start_span("sub-operation-1", parent_span=parent_span):
#             logger.debug("Executing sub-operation 1.", step="init")
#             # Simulate some work
#             logger.debug("Sub-operation 1 completed.", step="done")

#         with tracer.start_span("sub-operation-2", parent_span=parent_span):
#             logger.info("Executing sub-operation 2.", data_size=1024)
#             try:
#                 raise ValueError("Simulated error")
#             except ValueError as e:
#                 logger.error(f"Error in sub-operation 2: {e}", error_type="ValueError")

#         logger.info("Main operation finished.")