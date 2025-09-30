from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/greet/{name}")
def greet(name: str, age: int | None = None):
    return {"message": f"Hello {name}", "age": age}
