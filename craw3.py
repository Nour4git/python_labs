import os
import psutil
import asyncio
import requests
from xml.etree import ElementTree
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

def get_pydantic_ai_docs_urls():
    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
=        response = requests.get(sitemap_url)
        response.raise_for_status()  
        root = ElementTree.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        return [loc.text for loc in root.findall('.//ns:loc', namespace)]
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

async def crawl_parallel(urls: List[str], max_concurrent: int = 5):
    print("\n=== Parallel Crawling ===")
    peak_memory = 0
    process = psutil.Process(os.getpid())
    def log_memory(label: str):
        nonlocal peak_memory
        current = process.memory_info().rss
        if current > peak_memory:
            peak_memory = current
        print(f"{label} Memory: {current // (1024 * 1024)} MB (Peak: {peak_memory // (1024 * 1024)} MB)")

    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"]
    )
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        success, fail = 0, 0
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i:i + max_concurrent]
            print(f"Crawling batch {i // max_concurrent + 1} with {len(batch)} URLs")
            tasks = [
                crawler.arun(url=u, config=crawl_config, session_id=f"sess{i+j}")
                for j, u in enumerate(batch)
            ]

            log_memory(f"Before batch {i // max_concurrent + 1}")
            results = await asyncio.gather(*tasks, return_exceptions=True)
            log_memory(f"After batch {i // max_concurrent + 1}")

            for url, res in zip(batch, results):
                if isinstance(res, Exception):
                    print(f"Error crawling {url}: {res}")
                    fail += 1
                elif res.success:
                    print(f"Success: {url}")
                    success += 1
                else:
                    print(f"Fail: {url} | Error: {res.error_message}")
                    fail += 1

        print(f"\n✅ Success: {success} | ❌ Failed: {fail}")
    finally:
        await crawler.close()
        log_memory("Final")

async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs.")
        await crawl_parallel(urls, max_concurrent=10)
    else:
        print("No URLs found.")
if __name__ == "__main__":
    asyncio.run(main())
