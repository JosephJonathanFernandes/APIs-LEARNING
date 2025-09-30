import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/wait")
async def wait_example():
    await asyncio.sleep(2)  # simulate long task
    return {"message": "Finished waiting!"}
