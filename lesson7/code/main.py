import requests

url = "https://www.baidu.com/"

params={
    'tn': '68018901_16_pg',
}

_headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}

resp = requests.get(url,headers=_headers,params=params,timeout=10)

print("这是resp: ",resp)
print("这是resp.status_code: ",resp.status_code)
print("这是resp.encoding: ",resp.encoding)
print("\n\n这是resp.text: ",resp.text)
print("\n\n这是resp.content: ",resp.content)
