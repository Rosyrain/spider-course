# -*- coding:utf-8 -*-
import requests, os
from bs4 import BeautifulSoup


class Image(object):
    def __init__(self):
        self.url = "https://www.duitang.com/search/?kw=%E5%A4%95%E9%98%B3&type=feed"
        self.number = 1
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

    def get_data_index(self):
        response = requests.get(url=self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_data_index(self, response):
        soup = BeautifulSoup(response, "lxml")
        image_data_list = soup.find_all("img", alt="夕阳")
        for data in image_data_list:
            href = data.get("src")
            self.write_image_girl(href)

    def write_image_girl(self, href):
        with open("./image/%d" % self.number + os.path.splitext(href)[-1], "wb") as f:
            resp = requests.get(href)
            f.write(resp.content)
            print(f"第-{self.number}-张图片保存完毕")
            self.number += 1

    def run(self):
        response = self.get_data_index()
        self.parse_data_index(response)


if __name__ == '__main__':
    spider = Image()
    spider.run()
