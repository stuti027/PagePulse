# PagePulse

PagePulse is a lightweight webpage analysis tool that provides a quick health check for any public webpage.

Enter a URL and PagePulse analyzes key performance, content, and accessibility-related metrics and presents them in a simple report.

## Features

PagePulse reports:

- HTTP status code
- Response time
- Page title
- Meta description
- Number of H1 headings
- Images with missing or empty alt text
- Approximate word count

It also handles invalid URLs, request timeouts, connection failures, and non-HTML resources.

## Tech Stack

- **Backend:** Python, FastAPI
- **HTTP Client:** HTTPX
- **HTML Parsing:** BeautifulSoup
- **Frontend:** HTML, CSS, JavaScript
- **Validation:** Pydantic
- **Testing:** pytest

## How It Works

The application follows a simple request pipeline:

```text
URL submitted by user
        ↓
FastAPI validates URL
        ↓
HTTPX fetches webpage
        ↓
Content-Type is validated
        ↓
BeautifulSoup parses HTML
        ↓
Page metrics are extracted
        ↓
FastAPI returns JSON
        ↓
Frontend displays report
```

## API

### Analyze a webpage

```http
GET /analyze?url=https://example.com
```

### Successful response

```json
{
  "url": "https://example.com/",
  "status_code": 200,
  "response_time_ms": 152.41,
  "title": "Example Domain",
  "meta_description": null,
  "h1_count": 1,
  "images_missing_alt": 0,
  "word_count": 28
}
```

### Error responses

| Status | Meaning |
| --- | --- |
| `422` | Invalid URL |
| `415` | Resource is not an HTML webpage |
| `502` | Unable to connect to the target website |
| `504` | Target website timed out |

Interactive FastAPI documentation is also available at:

```text
/docs
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/stuti027/PagePulse
cd PagePulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Testing

Run the test suite with:

```bash
pytest
```

The parsing tests use controlled HTML fixtures rather than live websites so that changes to external webpages or network conditions do not make the tests nondeterministic.

The tests cover:

- Standard HTML parsing
- Missing page metadata
- Missing and empty image alt attributes

## Design Decisions

### 1. Separating fetching from HTML parsing

The HTTP request logic is handled by `analyze_page()`, while HTML metric extraction is handled separately by `parse_html()`.

This keeps networking concerns separate from parsing logic and makes the parser independently testable without requiring live HTTP requests.

### 2. Using FastAPI and Pydantic for the API boundary

FastAPI provides a lightweight API layer, while Pydantic's `HttpUrl` validation rejects malformed URLs before they reach the analysis service.

Different failure conditions are mapped to meaningful HTTP status codes instead of returning a generic error for every failure.

### 3. Keeping the frontend and API in one application

PagePulse uses a small vanilla HTML/CSS/JavaScript frontend served directly by FastAPI.

For the scope of this task, a separate frontend framework and deployment would introduce unnecessary complexity. Keeping both layers together makes the application easier to run and deploy while maintaining separation between the UI, API, and analysis logic.

## AI Usage

AI assistance was used during development for brainstorming implementation approaches, reviewing code structure, and iterating on the frontend styling.

I reviewed and adapted the generated suggestions rather than using them unchanged. In particular, I separated the webpage fetching and parsing logic to improve testability, refined error handling around URL validation and content types, and iterated on the interface and interaction design to better fit the scope of the application.

## Limitations and Future Improvements

PagePulse currently analyzes the HTML returned directly by the target server. Content rendered dynamically through client-side JavaScript may therefore not be represented fully in the analysis.

With more time, I would add browser-based rendering for JavaScript-heavy pages and expand the analysis with metrics such as heading hierarchy, broken links, accessibility checks, and additional performance indicators.

---

Built for Digital Heroes Training Task.