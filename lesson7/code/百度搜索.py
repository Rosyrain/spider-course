import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
}
params = {
    'wd': 'G.E.M.邓紫棋',
}

# url = 'http://www.baidu.com/s?wd=G.E.M.%E9%82%93%E7%B4%AB%E6%A3%8B&rsv_spt=1&rsv_iqid=0xe5d6b2cc00001bc2&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=68018901_16_pg&rsv_enter=1&rsv_dl=tb&oq=G%2526gt%253BM&rsv_btype=t&inputT=3373&rsv_t=eee1C7sFt%2BmVRpzKgxMwjkisut2upt%2B4YyoV7I2WYhBXX1ZbRnpJ01O5MkUrvCh3yq31b%2FM&rsv_sug3=14&rsv_sug1=9&rsv_sug7=100&rsv_pq=e6cbae7a0014dda1&rsv_sug2=0&rsv_sug4=4450'

response = requests.get(url='http://www.baidu.com/s',params=params,headers=headers)
response.encoding = 'utf-8'
print(response.text)