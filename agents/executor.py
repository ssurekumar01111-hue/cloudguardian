from google.adk.agents import LlmAgent
from ..telemetry import tracer

with tracer.start_as_current_span("agent.init") as span:
    span.set_attribute("agent.name", "executor_agent")
    executor_agent = LlmAgent(
        name='executor_agent',
        model='gemini-2.5-flash',
        description='Executes approved remediations and monitors recovery.',
        instruction="""You are ExecutorAgent responsible for executing 
approved remediations.

When given an approved remediation action:
1. Confirm the approved action clearly
2. Describe the execution steps you are performing
3. Report the execution result as: SUCCESS or IN_PROGRESS
4. List what was done:
   - Action taken
   - Timestamp
   - Expected recovery time
5. Transfer to reporter_agent with execution summary

IMPORTANT: You do not call external tools. You confirm and 
document the execution of the approved remediation.
Always transfer to reporter_agent when done.""",
        tools=[],
    )
