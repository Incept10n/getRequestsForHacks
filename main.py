from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from collections import deque

app = FastAPI()
last_requests = deque(maxlen=10)

@app.get("/")
async def main_get(urlParams: str = Query(None)):
    last_requests.append(urlParams)
    return JSONResponse(content={"last_requests": list(last_requests)})
