from ..telemetry import tracer
import time
from google.adk.agents import LlmAgent

def on_agent_start(session_id: str):
    with tracer.start_as_current_span("remediation_agent.execute") as span:
        span.set_attribute("session.id", session_id)
        span.set_attribute("agent.name", "remediation_agent")
        span.set_attribute("mcp.server", "dynatrace")
        span.set_attribute("timestamp", time.time())

with tracer.start_as_current_span("agent.init") as span:
    span.set_attribute("agent.name", "remediation_agent")
    remediation_agent = LlmAgent(
        name='remediation_agent',
        model='gemini-2.5-flash',
        description='Generates fix options and risk assessments.',
        instruction="""Generate 2-3 fix options with success probability and risk level. 
Set requires_approval=true for High risk actions.""",
        tools=[],
    )
