import time

from playwright.sync_api import sync_playwright
def get_title_sync(urls):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            page.goto(url)
            print(f"{url} -> {page.title()}")

        browser.close()
urls = ["https://www.baidu.com", "https://www.bing.com", "https://www.sougou.com"]
t1 = time.time()
print("开始运行")
get_title_sync(urls)
print(f"运行结束，耗时:{time.time() - t1}")