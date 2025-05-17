import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.add_init_script("./3_3_6_stealth.min.js")
        page = await context.new_page()

        await page.goto("https://baidu.com")
        print(f"title:{await page.title()}")

async def run_js_code():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="storage.json")
        page = await context.new_page()

        await page.goto("https://www.bilibili.com")

        title = await page.evaluate("() => document.title")
        print(f"页面标题是：{title}")

        # 模拟修改 DOM
        await page.evaluate("""
            () => {
                let h = document.createElement('h1');
                h.innerText = "✨ Hello from injected JS!";
                h.style.color = "red";
                document.body.prepend(h);
            }
        """)

        await browser.close()

if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()