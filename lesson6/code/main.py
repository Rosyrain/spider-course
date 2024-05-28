import urllib

import requests
import json
from pyecharts.charts import Line
from pyecharts.options import TitleOpts, ToolboxOpts, LegendOpts, InitOpts, DataZoomOpts
import pandas as pd

url = 'http://www.xinfadi.com.cn/getPriceData.html'

_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Content-Length': '140',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.xinfadi.com.cn',
    'Origin': 'http://www.xinfadi.com.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
}

# data = 'limit=20&current=1&pubDateStartTime=2024%2F05%2F01&pubDateEndTime=2024%2F05%2F28&prodPcatid=&prodCatid=&prodName=%E5%A4%A7%E7%99%BD%E8%8F%9C'
data = {
    'limit':'20',
    'current':'1',
    'pubDateStartTime':'2024/05/01',
    'pubDateEndTime':'2024/05/28',
    'prodPcatid':'',
    'prodCatid':'',
    'prodName':'大白菜',
}

resp = requests.post(url,headers=_headers,data=urllib.parse.urlencode(data))
content = resp.content
# print(content)

data = json.loads(content)
# print(data)

# 提取所需信息
prod_name = data['list'][0]['prodName']
low_prices = [float(item['lowPrice']) for item in data['list']]
high_prices = [float(item['highPrice']) for item in data['list']]
avg_prices = [float(item['avgPrice']) for item in data['list']]
places = [item['place'] for item in data['list']]
pub_dates = [item['pubDate'].split(' ')[0] for item in data['list']]

# 创建 DataFrame
df = pd.DataFrame({
    '蔬菜名称': [prod_name] * len(low_prices),
    '最低价格': low_prices,
    '最高价格': high_prices,
    '平均价格': avg_prices,
    '产地': places,
    '日期': pub_dates
})

# 写入 Excel 文件
df.to_excel('vegetable_price_data.xlsx', index=False)
print('数据已成功写入 vegetable_price_data.xlsx 文件中。')

# 创建 Line 图
line = Line(init_opts=InitOpts(width='1000px', height='600px'))
line.add_xaxis(pub_dates)
line.add_yaxis('最低价格', low_prices)
line.add_yaxis('最高价格', high_prices)
line.add_yaxis('平均价格', avg_prices)

# 设置标题、工具栏、图例和滑动选择框
line.set_global_opts(
    title_opts=TitleOpts(title=f'{prod_name}价格波动图'),
    toolbox_opts=ToolboxOpts(pos_left='auto',pos_right='auto',pos_bottom="auto",pos_top="20px"),
    legend_opts=LegendOpts(),
    datazoom_opts=[
        DataZoomOpts(
            is_show=True,
            type_='slider',
            xaxis_index=[0],
            range_start=0,
            range_end=100
        )
    ]
)

# 渲染图表
line.render('vegetable_price_chart.html')
print('价格波动图已成功生成为 vegetable_price_chart.html 文件。')