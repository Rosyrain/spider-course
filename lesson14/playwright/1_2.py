import time
import asyncio
from playwright.async_api import async_playwright


async def get_title(page, url):
    await page.goto(url)
    title = await page.title()
    print(f"{url} -> {title}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        urls = ["https://www.baidu.com", "https://www.bing.com", "https://www.sougou.com"]
        pages = [await context.new_page() for _ in urls]

        # 同时并发访问所有页面
        tasks = [get_title(page, url) for page, url in zip(pages, urls)]
        await asyncio.gather(*tasks)

        await browser.close()

t1 = time.time()
print("开始运行")
asyncio.run(main())
print(f"运行结束，耗时:{time.time() - t1}")
