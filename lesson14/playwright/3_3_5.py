# 是否开启无头模式
HEADLESS = False

# 平台
PLATFORM = "bilibili"

# 是否保存登录状态
SAVE_LOGIN_STATE = True

# 用户浏览器缓存的浏览器文件配置
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

import os
import sys
import asyncio
from typing import Optional,Dict,List,Tuple
from playwright.async_api import async_playwright
from playwright.async_api import (BrowserContext, BrowserType, Page, async_playwright,Cookie)


async def main():
    async with async_playwright() as p:
        chromium = p.chromium
        browser_context = await launch_browser(chromium,None, None, headless=False)
        page = await browser_context.new_page()

async def launch_browser(
        chromium: BrowserType,
        playwright_proxy: Optional[Dict], # [{"http":"http://ip:port","https":"https://ip:port"},... ...]
        user_agent: Optional[str],  # ua列表
        headless: bool = True   # 无头模式
) -> BrowserContext:
    """
    launch browser and create browser context
    :param chromium: chromium browser
    :param playwright_proxy: playwright proxy
    :param user_agent: user agent
    :param headless: headless mode
    :return: browser context
    """

    if SAVE_LOGIN_STATE:
        # feat issue #14
        # we will save login state to avoid login every time
        user_data_dir = os.path.join(os.getcwd(), "browser_data",
                                     config.USER_DATA_DIR % PLATFORM)  # type: ignore
        browser_context = await chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            accept_downloads=True,
            headless=headless,
            proxy=playwright_proxy,  # type: ignore
            viewport={"width": 1920, "height": 1080},
            user_agent=user_agent
        )
        return browser_context
    else:
        # type: ignore
        browser = await chromium.launch(headless=headless, proxy=playwright_proxy)
        browser_context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=user_agent
        )
        return browser_context

def convert_cookies(cookies: Optional[List[Cookie]]) -> Tuple[str, Dict]:
    if not cookies:
        return "", {}
    cookies_str = ";".join([f"{cookie.get('name')}={cookie.get('value')}" for cookie in cookies])
    cookie_dict = dict()
    for cookie in cookies:
        cookie_dict[cookie.get('name')] = cookie.get('value')
    return cookies_str, cookie_dict


def convert_str_cookie_to_dict(cookie_str: str) -> Dict:
    cookie_dict: Dict[str, str] = dict()
    if not cookie_str:
        return cookie_dict
    for cookie in cookie_str.split(";"):
        cookie = cookie.strip()
        if not cookie:
            continue
        cookie_list = cookie.split("=")
        if len(cookie_list) != 2:
            continue
        cookie_value = cookie_list[1]
        if isinstance(cookie_value, list):
            cookie_value = "".join(cookie_value)
        cookie_dict[cookie_list[0]] = cookie_value
    return cookie_dict

if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
