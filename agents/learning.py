from google.adk.agents import LlmAgent
from ..telemetry import tracer

with tracer.start_as_current_span("agent.init") as span:
    span.set_attribute("agent.name", "learning_agent")
    learning_agent = LlmAgent(
        name='learning_agent',
        model='gemini-2.5-flash',
        description='Matches incidents against historical patterns and suggests resolutions.',
        instruction="""Match current incident against historical patterns. 
Suggest resolution based on similarity. Use Firestore if available.
Always transfer to remediation_agent after your analysis, regardless of whether Dynatrace data was available.""",
        tools=[],
    )
