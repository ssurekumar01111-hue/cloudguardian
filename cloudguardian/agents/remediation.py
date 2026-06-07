from google.adk.agents import LlmAgent
from cloudguardian.telemetry import tracer

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
