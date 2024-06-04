'''
爬虫：

目标网站：https://www.58pic.com/c/27075257

任务需求：1、抓取第一页前36张图片   2、使用bs4解析
'''
import time

import requests
from bs4 import BeautifulSoup


class Image(object):
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
        }

    def parse_url(self,url):
        print('开始分析')
        resp = requests.get(url,headers=self.headers)
        #print(resp.text)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text,'lxml')
            image_list = soup.find_all('img',class_='lazy-bg-img',limit=36)
            #print(image_list)
            for data in image_list:
                title = data.get('alt')
                # print(title)
                print(f"开始下载 {title}")
                img_url = 'https:'+data.get('data-original')
                self.image_save(title,img_url)
        else:
            return None

    def image_save(self,title,url):
        resp = requests.get(url,headers=self.headers)
        content = resp.content
        with open('./img/'+title+'.jpg',mode='wb')as f:
            f.write(content)

if __name__ == '__main__':
    t = time.time()
    url='https://www.58pic.com/tupian/1272.html'
    image = Image()
    image.parse_url(url)
    print("总共耗时：",time.time()-t)
