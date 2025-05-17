import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://bilibili.com")
        await page.click('xpath=//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]')
        await page.fill('xpath=/html/body/div[4]/div/div[4]/div[2]/form/div[1]/input','account')
        await page.fill('xpath=/html/body/div[4]/div/div[4]/div[2]/form/div[3]/input','password')
        await page.click('xpath=/html/body/div[4]/div/div[4]/div[3]/div[2]/div[3]')

        # await page.uncheck('xpath=//*[@id="select_all"]')
        await asyncio.sleep(3)
        await page.goto('https://www.hostize.com/zh/')
        await page.set_input_files('xpath=//*[@id="file-upload"]','./3_3_2.py')

        el = await page.query_selector('xpath=/html/body/app-root/ng-component/app-page/div/app-header/app-langs/div/div[2]/div/div/div[2]/a[8]')
        if el:
            href = await el.get_attribute('href')
            text = await el.text_content()
            print(text,href)
        await asyncio.sleep(2000)
        await browser.close()

asyncio.run(main())