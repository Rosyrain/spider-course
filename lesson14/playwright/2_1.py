import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://baidu.com")
        title = await page.title()
        print(title)
asyncio.run(main())