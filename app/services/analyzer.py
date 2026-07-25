import time

import httpx
from bs4 import BeautifulSoup


def analyze_page(url: str):
    start_time = time.perf_counter()

    response = httpx.get(
        url,
        follow_redirects=True,
        timeout=10.0
    )

    response_time = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    content_type = response.headers.get("content-type", "")

    if "text/html" not in content_type.lower():
        raise ValueError("The URL does not point to an HTML page.")

    soup = BeautifulSoup(response.text, "html.parser")

    title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else None
    )

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = (
        meta_tag.get("content", "").strip()
        if meta_tag
        else None
    )

    h1_count = len(soup.find_all("h1"))

    images = soup.find_all("img")
    images_missing_alt = sum(
        1
        for image in images
        if not image.get("alt", "").strip()
    )

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text(" ", strip=True)
    word_count = len(text.split())

    return {
        "url": str(response.url),
        "status_code": response.status_code,
        "response_time_ms": response_time,
        "title": title,
        "meta_description": meta_description,
        "h1_count": h1_count,
        "images_missing_alt": images_missing_alt,
        "word_count": word_count,
    }