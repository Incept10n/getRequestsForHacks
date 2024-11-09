from fastapi import FastAPI
from fastapi.responses import JSONResponse
from collections import deque

app = FastAPI()
last_requests = deque(maxlen=10)

@app.get("/{path:path}")  
async def main_get(path: str):
    last_requests.append(path)
    return JSONResponse(content={"last_requests": list(last_requests)})
