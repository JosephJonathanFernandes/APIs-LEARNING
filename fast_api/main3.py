from fastapi import Depends, FastAPI

app = FastAPI()

# Example: a reusable dependency
def get_token_header(token: str):
    if token != "secret123":
        raise HTTPException(status_code=400, detail="Invalid Token")
    return token

@app.get("/protected")
def protected_route(token: str = Depends(get_token_header)):
    return {"message": "You are authorized", "token": token}
