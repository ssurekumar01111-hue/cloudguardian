from ..telemetry import tracer
import time
from google.adk.agents import LlmAgent

def on_agent_start(session_id: str):
    with tracer.start_as_current_span("reporter_agent.execute") as span:
        span.set_attribute("session.id", session_id)
        span.set_attribute("agent.name", "reporter_agent")
        span.set_attribute("mcp.server", "dynatrace")
        span.set_attribute("timestamp", time.time())

with tracer.start_as_current_span("agent.init") as span:
    span.set_attribute("agent.name", "reporter_agent")
    reporter_agent = LlmAgent(
        name='reporter_agent',
        model='gemini-2.5-flash',
        description='Generates postmortem reports and assigns incident IDs.',
        instruction="""You are ReporterAgent responsible for generating 
incident postmortems.

When given an incident summary, generate a postmortem with:
- Incident ID: INC-YYYYMMDD-NNN format
- Timeline of events
- Root cause analysis  
- Business impact assessment
- Remediation actions taken
- Prevention recommendations

Format the report clearly with sections.
Do not call any tools. Generate the report from context provided.""",
        tools=[],
    )
