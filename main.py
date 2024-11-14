from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from collections import deque

app = FastAPI()

last_requests = deque(maxlen=5)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=JSONResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/requests")
async def get_last_requests():
    return JSONResponse(content={"last_5_requests": list(last_requests)})

@app.get("/{path:path}")
async def catch_all_paths(path: str, request: Request):
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host,
        "cookies": request.cookies,
        "query_params": dict(request.query_params) if request.query_params else {},
    }
    
    last_requests.append(request_info)

    return {"message": "Request recorded", "path": path}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all_paths(path: str, request: Request):
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host,
        "cookies": request.cookies,
        "query_params": dict(request.query_params) if request.query_params else {},
        "body": None,
    }

    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            request_info["body"] = await request.json()  # Читаем тело как JSON
        except Exception as e:
            request_info["body"] = {"error": f"Failed to parse body: {str(e)}"}

    last_requests.append(request_info)

    return {"message": "Request recorded", "path": path, "method": request.method, "body": request_info["body"]}