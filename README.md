# CloudGuardian 🛡️

**Autonomous Reliability Engineer powered by Google Cloud ADK + Dynatrace MCP**

Built for the Google Cloud Rapid Agent Hackathon — Dynatrace Track

## What it does
CloudGuardian is a 7-agent autonomous system that monitors your 
infrastructure via Dynatrace, investigates incidents, proposes 
remediations with human approval gates, executes fixes, and 
generates postmortems automatically.

## Key Capabilities
✓ Monitor Dynatrace for active problems via MCP
✓ Investigate root cause using live DQL queries  
✓ Match against historical incident patterns
✓ Propose remediation options with risk/success scores
✓ Require human approval before executing changes
✓ Execute approved remediations autonomously
✓ Generate structured postmortems automatically
✓ Ship agent traces to Dynatrace via OpenTelemetry

## Architecture
![CloudGuardian Architecture](docs/architecture.png)

- **Supervisor** — orchestrates the full workflow
- **WatcherAgent** — monitors Dynatrace for active problems
- **TriageAgent** — investigates root cause using DQL queries
- **LearningAgent** — matches against historical patterns
- **RemediationAgent** — proposes fixes with risk/success scores
- **ExecutorAgent** — executes approved remediations
- **ReporterAgent** — generates incident postmortems

## Tech Stack
- Google Cloud ADK 2.1.0
- Gemini 2.5 Flash
- Dynatrace MCP Server (stdio)
- Vertex AI Agent Platform
- Cloud Run
- OpenTelemetry → Dynatrace

## Agent Builder Integration
CloudGuardian is built with Google Cloud Agent Builder framework 
(ADK 2.1.0) — the official SDK for Vertex AI Agent Platform. 
The cloudguardian-supervisor agent is registered on Agent Platform 
and the full 7-agent system runs via ADK runtime on Cloud Run.


## Live Demo
- Web UI: https://cloudguardian-ui-118329824935.us-central1.run.app

- Demo Video: https://youtu.be/800y9S81vOM

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # add your tokens
adk web
```

## License
MIT
