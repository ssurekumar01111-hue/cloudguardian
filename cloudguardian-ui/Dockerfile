FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn httpx python-multipart
COPY . .
EXPOSE 8080
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]