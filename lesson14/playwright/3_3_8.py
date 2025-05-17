import asyncio
import re

from playwright.async_api import async_playwright

async def cancel_request(route, request):
    print(f"url-->{request.url}")
    route.abort()

async def on_response(request):
    response = await request.response()
    print(f"status-->{response.status}  url-->{request.url}")

# 主函数
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context()

        # JS 注入（比如防检测）
        await context.add_init_script(path="3_3_6_stealth.min.js")

        page = await context.new_page()
        page.on("requestfinished", on_response)

        await page.route(re.compile(r"(\.png)|(\.jpg)"), cancel_request)
        await page.goto("https://www.xiaohongshu.com/explore",timeout=60000)
        await page.wait_for_load_state('networkidle')

        await browser.close()

# 启动程序
asyncio.run(main())
