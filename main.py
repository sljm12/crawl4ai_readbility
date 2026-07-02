import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, AnyHttpUrl

from crawler import _crawl

load_dotenv()

CRAWL4AI_DEBUG = os.getenv("CRAWL4AI_DEBUG", "false").lower() == "true"

app = FastAPI(
    title="Crawl4AI Readability API",
    description="Extract readable article content from any URL as Markdown",
    version="1.0.0",
)


class CrawlRequest(BaseModel):
    url: AnyHttpUrl


class CrawlResponse(BaseModel):
    success: bool
    url: str
    content: str


@app.post("/api/crawl", response_model=CrawlResponse)
async def crawl_endpoint(request: CrawlRequest):
    try:
        _, _, markdown = await _crawl(str(request.url))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    return CrawlResponse(success=True, url=str(request.url), content=markdown)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail},
    )


@app.get("/")
async def root():
    return {
        "service": "Crawl4AI Readability API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/crawl": "Extract article content from a URL",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=CRAWL4AI_DEBUG)
