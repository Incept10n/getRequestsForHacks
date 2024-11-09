from fastapi import FastAPI
from fastapi import Query

app = FastAPI()

@app.get("/")
async def main_get(urlParams: str = Query(None)):
    return {"url params": urlParams}
