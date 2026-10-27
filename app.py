from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from config import settings
from security import encode, decode
from agent import get_document, save_db

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/health")
def get_health():
    return {"response": "app is running"}

@app.post("/login", description="Login endpoint")
def get_login(form: OAuth2PasswordRequestForm = Depends()):
    username = form.username
    password = form.password
    if username != settings.user_name or password != settings.password:
        return {"status": 401, "response": "Invalid details"}
    token = encode(username, settings.jwt_secret, settings.algo)
    return {"status": 200, "access_token": token, "token_type": "bearer"}

@app.post("/agent", description="Protected endpoint")
def get_protected(query: str, file: UploadFile = File, token: str = Depends(oauth2_scheme)):
    payload = decode(token, settings.jwt_secret, settings.algo)
    if payload == "Error":
        return {"status": 401, "response": "Unauthorized"}
    if payload.get("role") != "ADMIN":
        return {"status": 403, "response": "Forbidden"}
    result = get_document(file.file)
    docs = save_db(result, query)
    return {"status": 200, "response": docs}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)