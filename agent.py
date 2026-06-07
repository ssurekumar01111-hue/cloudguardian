from google.adk.agents import LlmAgent
from .agents.watcher import watcher_agent
from .agents.triage import triage_agent
from .agents.learning import learning_agent
from .agents.remediation import remediation_agent
from .agents.executor import executor_agent
from .agents.reporter import reporter_agent
from .telemetry import tracer
from google.adk.agents.callback_context import CallbackContext
import time

with tracer.start_as_current_span("cloudguardian.startup") as span:
    span.set_attribute("agent.name", "cloudguardian_supervisor")
    span.set_attribute("agents.count", 7)
    span.set_attribute("mcp.server", "dynatrace")

    root_agent = LlmAgent(
        name='cloudguardian_supervisor',
        model='gemini-2.5-flash',
        description=(
            'Autonomous Reliability Engineer that predicts outages, investigates '
            'incidents, learns from history, simulates fixes, and executes '
            'approved remediations using Dynatrace MCP.'
        ),
        instruction="""You are CloudGuardian Supervisor. You MUST delegate to sub-agents. Never answer directly.

ALWAYS follow this exact sequence:
1. Transfer to watcher_agent first — it checks Dynatrace for problems
2. Transfer to triage_agent — it investigates root cause  
3. Transfer to learning_agent — it checks historical patterns
4. Transfer to remediation_agent — it proposes fixes
5. Ask user to approve the fix
6. Transfer to executor_agent — it executes approved fix
7. Transfer to reporter_agent — it writes the postmortem

If triage_agent reports an entity is not found in Dynatrace, continue the workflow anyway. Transfer to learning_agent, then remediation_agent to propose fixes based on reported symptoms. Never terminate an investigation early — always complete the full chain through to reporter_agent.

Start immediately. Transfer to watcher_agent now.""",
        tools=[],
        sub_agents=[
            watcher_agent,
            triage_agent,
            learning_agent,
            remediation_agent,
            executor_agent,
            reporter_agent
        ],
    )

def before_model_callback(callback_context: CallbackContext, **kwargs):
    try:
        span = tracer.start_span("cloudguardian.model_call")
        agent_name = getattr(callback_context, 'agent_name', None)
        if not agent_name and hasattr(callback_context, 'agent'):
            agent_name = getattr(callback_context.agent, 'name', 'unknown')
        
        span.set_attribute("agent.name", str(agent_name or "unknown"))
        span.set_attribute("session.id", str(getattr(callback_context, 'session_id', 'unknown')))
        span.set_attribute("timestamp", time.time())
        span.end()
    except Exception as e:
        print(f"OTEL CALLBACK ERROR: {e}", file=sys.stderr, flush=True)
    return None

root_agent.before_model_callback = before_model_callback
