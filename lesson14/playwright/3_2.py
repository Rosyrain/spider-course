import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("NBA")
    page.locator("#kw").press("CapsLock")
    page.locator("#kw").fill("NBA排名")
    page.goto("http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=nba%E6%8E%92%E5%90%8D&fenlei=256&rsv_pq=0x8cc30d85063c7a80&rsv_t=e6c02Rfwvst%2F6FN9HVCbwx4kcnD9jZsz4W28bEWoUHac4rIlfbJS1AhduX1a&rqlang=en&rsv_dl=ib&rsv_sug3=11&rsv_sug1=2&rsv_sug7=100")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
