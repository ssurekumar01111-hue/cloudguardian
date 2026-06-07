FROM python:3.11-slim

# Install Node.js for Dynatrace MCP stdio server
RUN apt-get update && apt-get install -y nodejs npm curl && \
    npm install -g @dynatrace-oss/dynatrace-mcp-server && \
    apt-get clean

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8080"]
