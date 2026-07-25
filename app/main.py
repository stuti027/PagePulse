from fastapi import FastAPI

from app.services.analyzer import analyze_page


app = FastAPI(title="Page Pulse API")


@app.get("/")
def home():
    return {"message": "Page Pulse API is running"}


@app.get("/analyze")
def analyze(url: str):
    return analyze_page(url)