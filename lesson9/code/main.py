'''
爬虫

目标网站：https://cs.anjuke.com/sale/yuelu/

任务需求：

1. ​    使用xpath解析

2. ​    抓取第一页：标题，户型，面积，楼层，建造时间，位置，总价，单价
3. ​    要求存储在MySQL和MongoDB
'''


'''
第三页：https://cs.anjuke.com/sale/yuelu/p3/
第二页：https://cs.anjuke.com/sale/yuelu/p2/

所需数据在源代码上
'''
import pymysql
import pymongo
import requests
from lxml import etree
import pandas as pd

from pyecharts.charts import Page, Bar, Pie
from pyecharts.globals import ThemeType
import pyecharts.options as opts

class House(object):
    def __init__(self):
        # 创建链接
        self.conn = pymysql.Connect(
            host="127.0.0.1",  # 代表本机地址
            port=3306,  # MySQL默认端口
            user="root",  # 用户名 root是最高权限
            password="xxxxxx",  # 数据库的密码
            db="xxxx"  # 指定的数据库
        )
        # 创建游标，用于传递python给MySQL的命令和MySQL返回的内容
        self.cursor = self.conn.cursor()

        # 此为与mongodb数据库的连接
        self.client = pymongo.MongoClient(host='localhost',port=27017)
        self.db = self.client["xxxxxx"]

        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54'
        }

    def parse_url(self):
        url='https://cs.anjuke.com/sale/yuelu/'

        resp = requests.get(url,headers=self.headers)

        html = etree.HTML(resp.text)

        div_list = html.xpath('//div[@class="property"]')

        data=[]

        for div in div_list:
            item={}
            try:
                item['title'] = div.xpath('.//h3/text()')[0]
            except:
                item['title'] = '无标题信息'
            try:
                item['type'] = ''.join(div.xpath('.//p[@class="property-content-info-text property-content-info-attribute"]/span/text()'))
            except:
                item['type'] = '无户型信息'
            try:
                item['area'] = div.xpath('./a/div[2]/div[1]/section/div[1]/p[2]/text()')[0].replace('\n','').strip(' ')
            except:
                item['area'] = '无面积信息'
            try:
                item['floor'] = div.xpath('./a/div[2]/div[1]/section/div[1]/p[4]/text()')[0].replace('\n','').strip(' ')
            except:
                item['floor'] = '无楼层信息'
            try:
                item['build_time'] = div.xpath('./a/div[2]/div[1]/section/div[1]/p[5]/text()')[0].replace('\n','').strip(' ')
            except:
                item['build_time'] = '无建造时间信息'
            try:
                item['location'] = ''.join(div.xpath('./a/div[2]/div[1]/section/div[2]/p[2]//span/text()')).replace('\n','').strip(' ')
            except:
                item['location'] = '无位置信息'
            try:
                item['total_price'] =''.join(div.xpath('./a/div[2]/div[2]/p[1]//span/text()')).replace('\n','').strip(' ')
            except:
                item['total_price'] = '无总价信息'
            try:
                item['unit_price'] = div.xpath("./a/div[2]/div[2]/p[2]/text()")[0].replace('\n','').strip(' ')
            except:
                item['unit_price'] = '无单价信息'
            print(item)

            #存入mysql(逐条)
            #self.save_mysql(item)

            #存入json表单(逐条)
            #self.save_json(item)

            #存入mysql(逐条)
            # self.save_mongoDB(item)

            data.append(item)

        #存入excel(全部)
        df = self.save_excel(data)

        #绘图
        self.drawing(df)

    def save_mysql(self,item):
        sql = 'insert into anjuke_house_data(title,type,area,floor,build_time,location,total_price,unit_price)' \
              'values (%s,%s,%s,%s,%s,%s,%s,%s)'
        params = [(item['title'],item['type'],item['area'],item['floor'],item['build_time'],item['location'],item['total_price'],item['unit_price'])]
        self.cursor.executemany(sql,params)
        self.conn.commit()

    def save_json(self,item):
        with open('house_json_data.json','a',encoding='utf-8')as f:
            f.write(str(item)+'\n')

    def save_mongoDB(self,item):
        # print(item)
        self.db.anjuke_house_data.insert_one(item)

    def save_excel(self,data):
        df = pd.DataFrame(data)

        # 检查是否存在 Excel 文件,如果不存在则创建一个新的
        try:
            existing_df = pd.read_excel('data.xlsx')
            # 将新数据追加到现有 Excel 文件中
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            # 创建一个新的 Excel 文件
            pass

        df.to_excel('data.xlsx', index=False)
        print("保存数据至excel成功......")

        return df

    def drawing(self,df):
        # 创建Page对象
        page = Page(layout=Page.DraggablePageLayout)

        # 第一页:房源类型分布
        house_type_dist = (
            Pie()
            .add("", list(zip(df['type'].unique(), df['type'].value_counts().tolist())), radius=["40%", "70%"])
            .set_global_opts(
                title_opts=opts.TitleOpts(title="房源类型分布"),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="20%", pos_right="20%"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    formatter="{b}: {d}%"
                )
            )
        )
        page.add(house_type_dist)

        # 第二页:总价和单价分布
        total_price_dist = (
            Bar()
            .add_xaxis(list(df['total_price'].unique()))
            .add_yaxis("", df['total_price'].value_counts().tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="总价分布"))
        )
        unit_price_dist = (
            Bar()
            .add_xaxis(list(df['unit_price'].unique()))
            .add_yaxis("", df['unit_price'].value_counts().tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="单价分布"))
        )
        page.add(total_price_dist, unit_price_dist)

        # 第三页:面积和楼层分布
        area_dist = (
            Bar()
            .add_xaxis(list(df['area'].unique()))
            .add_yaxis("", df['area'].value_counts().tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="面积分布"))
        )
        floor_dist = (
            Pie()
            .add("", list(zip(df['floor'].unique(), df['floor'].value_counts().tolist())), radius=["40%", "70%"])
            .set_global_opts(
                title_opts=opts.TitleOpts(title="楼层分布"),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="20%", pos_right="20%"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    formatter="{b}: {d}%"
                )
            )
        )
        page.add(area_dist, floor_dist)

        # 渲染多页面图表
        page.render("house_data_visualization.html")
        print("图像绘制成功......")


if __name__ == '__main__':
    house = House()
    house.parse_url()