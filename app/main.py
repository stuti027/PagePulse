from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import HttpUrl
import httpx

from app.services.analyzer import analyze_page


app = FastAPI(title="Page Pulse API")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


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