import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree

def get_pydantic_ai_docs_urls():
    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        return [loc.text for loc in root.findall('.//ns:loc', namespace)]
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling ===")
    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"]
    )
    crawl_config = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator())
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    try:
        session_id = "session1"
        for url in urls:
            result = await crawler.arun(url=url, config=crawl_config, session_id=session_id)
            if result.success:
                print(f"Crawled: {url} | Length: {len(result.markdown.raw_markdown)}")
            else:
                print(f"Failed: {url} | Error: {result.error_message}")
    finally:
        await crawler.close()

async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        await crawl_sequential(urls)
    else:
        print("No URLs found.")

if __name__ == "__main__":
    asyncio.run(main())
