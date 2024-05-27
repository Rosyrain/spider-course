import requests
from lxml import etree
import pandas as pd

url = "https://www.baidu.com/"
_headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
resp = requests.get(url,headers=_headers)
resp.encoding = 'utf-8'
content = resp.content
# print(content)

html = etree.HTML(content)

logo_url ='https:'+ html.xpath('//img[@id="s_lg_img"]/@src')[0]
print(logo_url)

with open("./logo.img",mode='wb')as f:
    img_content = requests.get(logo_url).content
    f.write(img_content)


data = []
data_list = html.xpath('//ul[@id="hotsearch-content-wrapper"]//li')
for data_e in data_list:
    title = data_e.xpath('.//text()')[2]
    url = data_e.xpath('.//a/@href')[0]
    print(f"title: {title}\nurl: {url}")
    data.append({"title":title,"url":url})
df = pd.DataFrame(data)

# 检查是否存在 Excel 文件,如果不存在则创建一个新的
try:
    existing_df = pd.read_excel('data.xlsx')
    # 将新数据追加到现有 Excel 文件中
    df = pd.concat([existing_df, df], ignore_index=True)
except FileNotFoundError:
    # 创建一个新的 Excel 文件
    pass

# 将 DataFrame 写入 Excel 文件
df.to_excel('data.xlsx', index=False)