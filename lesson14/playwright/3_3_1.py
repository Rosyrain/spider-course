import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://baidu.com")
        logo = await page.query_selector('//*[@id="s_lg_img"]')
        await logo.screenshot(path="baidu_logo.png")

        input("Press enter to continue...")
        await browser.close()

asyncio.run(main())