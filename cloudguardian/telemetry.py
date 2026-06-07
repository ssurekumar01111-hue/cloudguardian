from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import os

def setup_telemetry():
    resource = Resource.create({
        "service.name": "cloudguardian",
        "service.version": "1.0.0",
        "deployment.environment": "production"
    })

    exporter = OTLPSpanExporter(
        endpoint="https://nzz44700.live.dynatrace.com/api/v2/otlp/v1/traces",
        headers={
            "Authorization": f"Api-Token {os.environ.get('DT_API_TOKEN', '')}"
        }
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer("cloudguardian")

tracer = setup_telemetry()
