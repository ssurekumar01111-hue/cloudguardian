from ..telemetry import tracer
import time
import os
import sys
import shutil
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

def on_agent_start(session_id: str):
    with tracer.start_as_current_span("triage_agent.execute") as span:
        span.set_attribute("session.id", session_id)
        span.set_attribute("agent.name", "triage_agent")
        span.set_attribute("mcp.server", "dynatrace")
        span.set_attribute("timestamp", time.time())

dt_env = os.environ.copy()
dt_env["DT_ENVIRONMENT"] = os.environ.get("DT_ENVIRONMENT", "")
dt_env["DT_PLATFORM_TOKEN"] = os.environ.get("DT_PLATFORM_TOKEN", "")
dt_env["DT_MCP_LOG_LEVEL"] = "ERROR"
dt_env["DT_MCP_DISABLE_TELEMETRY"] = "true"

WRAPPER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'mcp_wrapper.py'
)

dt_mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[WRAPPER_PATH],
            env=dt_env
        )
    )
)

with tracer.start_as_current_span("agent.init") as span:
    span.set_attribute("agent.name", "triage_agent")
    triage_agent = LlmAgent(
        name='triage_agent',
        model='gemini-2.5-flash',
        description='Investigates incidents, builds timelines, and identifies root causes.',
        instruction="""You are TriageAgent, a specialist in incident investigation.

When investigating an incident:
1. Use find_entity_by_name to look for the service in Dynatrace
2. Use list_problems to check for related problems
3. Use generate_dql_from_natural_language and execute_dql for metrics
4. If the entity is NOT found in Dynatrace or data is unavailable, 
   DO NOT loop back to supervisor. Instead:
   - State clearly: "Entity not found in Dynatrace monitoring"
   - Proceed with analysis based on reported symptoms
   - Build a timeline from the information provided
   - Assign a root cause hypothesis with confidence score
   - Transfer to learning_agent with your analysis
5. NEVER transfer back to cloudguardian_supervisor

Always complete your analysis and transfer to learning_agent.""",
        tools=[dt_mcp_toolset],
    )
