import os
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from readability import Document
from markdownify import markdownify as md

load_dotenv()

CRAWL4AI_DEBUG = os.getenv("CRAWL4AI_DEBUG", "false").lower() == "true"
CRAWL4AI_WAIT_TIME = int(os.getenv("CRAWL4AI_WAIT_TIME", "0"))


async def _crawl(url: str):
    """Internal: runs the crawler and returns (raw_crawl_result, summary_html, markdown)."""
    config = BrowserConfig(headless=not CRAWL4AI_DEBUG)
    async with AsyncWebCrawler(config=config) as crawler:
        crawler_config = CrawlerRunConfig(delay_before_return_html=CRAWL4AI_WAIT_TIME)
        result = await crawler.arun(url=url, config=crawler_config)
    if not result.success:
        raise RuntimeError(getattr(result, "error_message", "Unknown crawl error"))
    if not result.html:
        raise RuntimeError("No HTML content returned from URL")
    summary_html = Document(result.html).summary()
    markdown = md(summary_html)
    if not markdown.strip():
        raise RuntimeError("No readable article content found")
    return result, summary_html, markdown


async def crawl_article(url: str) -> str:
    """Crawls a single article and returns its markdown content."""
    _, _, markdown = await _crawl(url)
    return markdown


async def crawl_article_full(url: str) -> dict:
    """Crawls a single article and returns a dict with full info."""
    result, _, markdown = await _crawl(url)
    return {
        "success": True,
        "url": url,
        "content": markdown,
    }

