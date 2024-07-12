# '''
# 1、爬虫
#
# > 目标网站：https://movie.douban.com/top250?start=0&filter=
# >
# > 要求：抓取前三页的html数据并保存为html文件
# '''
import time
import requests
from lxml import etree
import random
import re


user_agent_list = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]


def parse_url(url):
    while True:
        print(f"开始请求{url}")
        time.sleep(3)
        url = url
        UA = random.choice(user_agent_list)
        # print(UA)

        _headers = {
            'Cookie': 'bid=QWUV40oy-FY; _pk_id.100001.4cf6=f2805921a5ad8609.1685872579.; ll="108309"; _vwo_uuid_v2=D12C7D490102E90C58FD2D45CA5ACB05B|01cb4d51178de9859d5df7992ca64578; douban-fav-remind=1; __utmv=30149280.27358; __utma=223695111.363614075.1685872580.1692524924.1692526991.12; viewed="35264301"; __utma=30149280.2127834450.1685872580.1695305505.1700229256.17; __utmz=30149280.1700229256.17.12.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ses.100001.4cf6=1; ap_v=0,6.0',
            "User-Agent": UA
        }
        resp = requests.get(url=url, headers=_headers)
        content = resp.text
        # print(content)
        if '你访问豆瓣的方式有点像机器人程序。为了保护用户的数据，请向我们证明你是人类:' not in content:
            html = etree.HTML(content)
            # 爬取数据所需
            obj_director = re.compile('导演: (.*?)\xa0', re.S)
            obj_actor = re.compile('主演: (.*)', re.S)
            obj_year = re.compile('(.*?)\xa0', re.S)
            boj_country = re.compile('\xa0/\xa0(.*?)\xa0/\xa0', re.S)

            data_list = html.xpath('//ol[@class="grid_view"]//li')
            # print(data_list)
            for data in data_list:
                movie_rank = data.xpath('.//em[@class=""]/text()')[0]
                movie_name = data.xpath('.//span[@class="title"]/text()')
                # data.xpath('.//p[@class=""]/text()')返回内容
                # ['\n                            导演: 马丁·布莱斯 Martin Brest\xa0\xa0\xa0主演: 阿尔·帕西诺 Al Pacino / 克里斯...', '\n                            1992\xa0/\xa0美国\xa0/\xa0剧情\n                        ']
                movie_director = data.xpath('.//p[@class=""]/text()')[0]
                movie_director = obj_director.findall(movie_director)[0]
                movie_actor = data.xpath('.//p[@class=""]/text()')[0]
                movie_actor = obj_actor.findall(movie_actor)[0]
                movie_year = data.xpath('.//p[@class=""]/text()')[1]
                movie_year = obj_year.findall(movie_year)[0].strip('\n                            ')
                movie_country = data.xpath('.//p[@class=""]/text()')[1]
                movie_country = boj_country.findall(movie_country)[0]

                print('\n')
                print('电影排名:', movie_rank)
                print('电影名称:', movie_name[0])
                print('电影导演:', movie_director)
                print('电影主演:', movie_actor)
                print('电影年份:', movie_year)
                print('电影国家:', movie_country)
                with open('豆瓣TOP250.txt','a+',encoding='utf-8')as f:
                    f.write('\n电影排名:'+ movie_rank +'\n电影名称:' + movie_name[0] +'\n电影导演:' + movie_director+'\n电影主演:'+ movie_actor + '\n电影年份:'+ movie_year+'\n电影国家:'+ movie_country+'\n')
            break


#单网页尝试
cur_page = 1
while True:
    print("开始请求")
    time.sleep(3)
    url = f'https://movie.douban.com/top250?start={(cur_page-1)*25}&filter='
    UA = random.choice(user_agent_list)
    # print(UA)
    _headers = {
        'Cookie':'bid=QWUV40oy-FY; _pk_id.100001.4cf6=f2805921a5ad8609.1685872579.; ll="108309"; _vwo_uuid_v2=D12C7D490102E90C58FD2D45CA5ACB05B|01cb4d51178de9859d5df7992ca64578; douban-fav-remind=1; dbcl2="273587585:LGbDVmaWfD8"; push_noty_num=0; push_doumail_num=0; __utmz=30149280.1692524870.12.8.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/top250; __utmv=30149280.27358; ck=_afb; __utma=30149280.2127834450.1685872580.1692524870.1692526982.13; __utmc=30149280; __utmt=1; __utmb=30149280.2.10.1692526982; __utma=223695111.363614075.1685872580.1692524924.1692526991.12; __utmb=223695111.0.10.1692526991; __utmc=223695111; __utmz=223695111.1692526991.12.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1692526991%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%3A%2F%2Fmovie.douban.com%2Ftop250%3Fstart%3D25%26filter%3D%22%5D; _pk_ses.100001.4cf6=1',
        "User-Agent": random.choice(user_agent_list)
    }
    resp = requests.get(url=url, headers=_headers)
    print(resp.status_code)
    if resp.status_code != 200 or cur_page>10:
        print("状态异常或无数据可爬取")
        break
    content = resp.text
    # print(content)
    if '你访问豆瓣的方式有点像机器人程序。为了保护用户的数据，请向我们证明你是人类:' not in content:
        html = etree.HTML(content)
        # 爬取数据所需
        obj_director = re.compile('导演: (.*?)\xa0', re.S)
        obj_actor = re.compile('主演: (.*)', re.S)
        obj_year = re.compile('(.*?)\xa0', re.S)
        boj_country = re.compile('\xa0/\xa0(.*?)\xa0/\xa0',re.S)

        data_list = html.xpath('//ol[@class="grid_view"]//li')
        #print(data_list)
        for data in data_list:

            movie_rank = data.xpath('.//em[@class=""]/text()')[0]
            movie_name = data.xpath('.//span[@class="title"]/text()')
            # data.xpath('.//p[@class=""]/text()')返回内容
            # ['\n                            导演: 马丁·布莱斯 Martin Brest\xa0\xa0\xa0主演: 阿尔·帕西诺 Al Pacino / 克里斯...', '\n                            1992\xa0/\xa0美国\xa0/\xa0剧情\n                        ']
            try:
                movie_director = data.xpath('.//p[@class=""]/text()')[0]
            except:
                movie_director = "空"
            try:
                movie_director = obj_director.findall(movie_director)[0]
            except:
                movie_director = "空"
            movie_actor = data.xpath('.//p[@class=""]/text()')[0]
            try:
                movie_actor = obj_actor.findall(movie_actor)[0]
            except:
                movie_actor = '空'
            movie_year = data.xpath('.//p[@class=""]/text()')[1]
            movie_year = obj_year.findall(movie_year)[0].strip('\n                            ')
            movie_country = data.xpath('.//p[@class=""]/text()')[1]
            movie_country = boj_country.findall(movie_country)[0]

            print('\n')
            print('电影排名:', movie_rank)
            print('电影名称:', movie_name[0])
            print('电影导演:', movie_director)
            print('电影主演:', movie_actor)
            print('电影年份:', movie_year)
            print('电影国家:', movie_country)
        cur_page +=1
    else:
        _headers["Cookie"]= str(input("更新cookie值: "))



