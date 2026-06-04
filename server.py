import asyncio
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

app = FastAPI(title="Crawl4AI Server")

class CrawlRequest(BaseModel):
    url: str

class CrawlResponse(BaseModel):
    success: bool
    html: str = ""
    markdown: str = ""
    error: str = ""

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/crawl")
async def crawl(request: CrawlRequest):
    try:
        browser_config = BrowserConfig(headless=True)
        crawler_config = CrawlerRunConfig()

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=request.url,
                config=crawler_config
            )
            return CrawlResponse(
                success=True,
                html=result.html[:50000] if result.html else "",
                markdown=result.markdown[:50000] if result.markdown else ""
            )
    except Exception as e:
        return CrawlResponse(success=False, error=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11235)
