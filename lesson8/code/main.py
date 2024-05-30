# -*- coding:utf-8 -*-
import requests
from lxml import etree


class DouGuo(object):
    def __init__(self):
        self.url = "https://www.douguo.com/caipu/%E5%AE%B6%E5%B8%B8%E8%8F%9C/0/20"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

    def get_data_index(self):
        response = requests.get(self.url, headers=self.headers)
        response.encoding="utf-8"
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_data_index(self, response):
        html = etree.HTML(response)
        data_list = html.xpath('//ul[@class="cook-list"]//li[@class="clearfix"]')
        for data in data_list:
            # 提取文本值
            title = data.xpath("./div/a/text()")[0]
            major = data.xpath("./div/p/text()")[0]
            # 提取属性值
            head = data.xpath("./div/div[2]/a/img/@alt")[0]
            score = data.xpath("./div/div[1]//span/text()")[0]
            print(f"title: {title}\nmajor: {major}\nhead:{head}\nscore:{score}\n\n")


    def run(self):
        response = self.get_data_index()
        # print(response)
        self.parse_data_index(response)


if __name__ == '__main__':
    spider = DouGuo()
    spider.run()
