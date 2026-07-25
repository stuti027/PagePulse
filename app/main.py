from fastapi import FastAPI

app = FastAPI(title="Page Pulse API")


@app.get("/")
def home():
    return {"message": "Page Pulse API is running"}