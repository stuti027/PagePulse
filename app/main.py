from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl
import httpx

from app.services.analyzer import analyze_page


app = FastAPI(title="Page Pulse API")


@app.get("/")
def home():
    return {"message": "Page Pulse API is running"}


@app.get("/analyze")
def analyze(url: HttpUrl):
    try:
        return analyze_page(str(url))

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The website took too long to respond."
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the website."
        )

    except ValueError as error:
        raise HTTPException(
            status_code=415,
            detail=str(error)
        )