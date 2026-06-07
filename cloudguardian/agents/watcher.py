from cloudguardian.telemetry import tracer
import time
import os
import sys
import shutil
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

def on_agent_start(session_id: str):
    with tracer.start_as_current_span("watcher_agent.execute") as span:
        span.set_attribute("session.id", session_id)
        span.set_attribute("agent.name", "watcher_agent")
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
    span.set_attribute("agent.name", "watcher_agent")
    watcher_agent = LlmAgent(
        name='watcher_agent',
        model='gemini-2.5-flash',
        description='Monitors Dynatrace for open problems and anomalies.',
        instruction="""Monitor Dynatrace for open problems and anomalies. 
Report findings as JSON with severity and affected services.
If no entity found in Dynatrace, report findings and transfer 
to triage_agent. NEVER loop back to supervisor.""",
        tools=[dt_mcp_toolset],
    )
