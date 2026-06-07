import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
API_BASE = "https://cloudguardian-118329824935.us-central1.run.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html") as f:
        return f.read()

@app.get("/list-apps")
async def list_apps():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{API_BASE}/list-apps")
        return JSONResponse(r.json())

@app.post("/run")
async def run(request: Request):
    body = await request.json()
    async with httpx.AsyncClient(timeout=httpx.Timeout(280.0)) as c:
        r = await c.post(f"{API_BASE}/run", json=body)
        try:
            return JSONResponse(r.json())
        except Exception:
            return JSONResponse(
                {"error": r.text}, 
                status_code=r.status_code
            )

@app.post("/apps/{path:path}")
async def apps_post(path: str, request: Request):
    body = await request.json()
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(f"{API_BASE}/apps/{path}", json=body)
        return JSONResponse(r.json())

@app.get("/apps/{path:path}")
async def apps_get(path: str):
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.get(f"{API_BASE}/apps/{path}")
        try:
            return JSONResponse(r.json())
        except Exception:
            return JSONResponse({"error": r.text}, status_code=r.status_code)