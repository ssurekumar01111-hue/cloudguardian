import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
from cloudguardian.telemetry import tracer

dt_env = os.environ.copy()
dt_env["DT_ENVIRONMENT"] = os.environ.get("DT_ENVIRONMENT", "")
dt_env["DT_PLATFORM_TOKEN"] = os.environ.get("DT_PLATFORM_TOKEN", "")
dt_env["DT_MCP_LOG_LEVEL"] = "ERROR"
dt_env["DT_MCP_DISABLE_TELEMETRY"] = "true"

wrapper_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'mcp_wrapper.py'))

dt_mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[wrapper_path],
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
