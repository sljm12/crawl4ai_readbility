# Crawl4AI Readability API

FastAPI service that crawls a URL, extracts its readable article content, and returns it as Markdown.

## Stack

- **crawl4ai** — headless browser-based web crawling
- **readability-lxml** — extracts the "reader view" HTML from a page
- **markdownify** — converts the extracted HTML to Markdown
- **FastAPI + uvicorn** — HTTP API layer
- **python-dotenv** — environment configuration

## Files

| File | Purpose |
|---|---|
| `main.py` | FastAPI app with `POST /api/crawl` endpoint |
| `crawler.py` | Standalone `crawl_article(url)` helper |
| `.env` | Config overrides |
| `requirements.txt` | Python dependencies |

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `CRAWL4AI_DEBUG` | `false` | When `true`, shows the browser window and enables hot reload |
| `CRAWL4AI_WAIT_TIME` | `7` | Seconds to wait before extracting HTML (allows JS to render) |

## Running

```bash
pip install -r requirements.txt
python main.py
# → http://localhost:8000
```

## API

### `POST /api/crawl`

```json
// Request
{ "url": "https://example.com/article" }

// Response (200)
{ "success": true, "url": "...", "content": "# Markdown..." }

// Response (4xx/5xx)
{ "success": false, "error": "message" }
```

### `GET /`

Returns service metadata and available endpoints.
