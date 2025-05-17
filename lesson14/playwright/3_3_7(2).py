import asyncio
import re
import random
from playwright.async_api import async_playwright

# 响应处理
async def on_response(response):
    # print(f"status-->{response.status}  url-->{response.url}")
    url = response.url
    if "aweme/v1/web/general/search/single/" in url:
        try:
            json_data = await response.json()
            print(f"捕获接口: {url}")
            print(json_data)
        except Exception as e:
            print(f"[解析失败] {url} -> {e}")


async def auto_scroll(page, scroll_count=10):
    """

    模拟自然滚动行为
    :param page: Playwright 页面对象
    :param scroll_count: 总滚动次数
    :param total_duration: 滚动总时长（秒）
    """
    for i in range(scroll_count):
        print(f"滚动次数: {i + 1}")

        # 随机生成每次滚动的总长度
        scroll_amount = random.randint(500, 1000)

        # 随机生成间隔次数
        # interval_count = random.randint(3, 6)  # 每次滚动分成3到6次小滚动

        # 每次小滚动的总长度需要达到或超过 scroll_amount
        current_scroll = 0
        while current_scroll < scroll_amount:
            # 随机生成每次小滚动的长度
            small_scroll = random.randint(50, 200)  # 每次小滚动的长度在50到200像素之间
            current_scroll += small_scroll

            # 模拟小滚动操作
            await page.mouse.wheel(0, small_scroll)
            await asyncio.sleep(random.uniform(0.1, 0.3))  # 每次小滚动的间隔时间

        # 每次大滚动完成后休息1-3秒
        await asyncio.sleep(random.uniform(1, 3))


# 主函数
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context()

        # JS 注入（比如防检测）
        await context.add_init_script(path="3_3_6_stealth.min.js")

        page = await context.new_page()
        page.on("response", on_response)

        await page.goto("https://www.douyin.com", timeout=60000)
        await page.wait_for_load_state('load')
        input("请登录")
        print("开始自动滚动页面")
        await auto_scroll(page,scroll_count=10)
        print("滚动结束")
        await asyncio.sleep(2000)
        await browser.close()

# 启动程序
asyncio.run(main())
