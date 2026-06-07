FROM python:3.11-slim

# Install Node.js 22 for Dynatrace MCP stdio server
RUN apt-get update && apt-get install -y curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install -y nodejs && \
    npm install -g @dynatrace-oss/dynatrace-mcp-server && \
    apt-get clean

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8080", \
     "--allow_origins", "https://cloudguardian-ui-118329824935.us-central1.run.app"]