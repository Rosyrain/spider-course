# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
    <body>
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
            and they lived at the bottom of a well.
        </p>

<p class="story">...</p>
"""

# 创建对象
soup = BeautifulSoup(html_doc, "lxml")
# 格式化输出
# print(soup.prettify())

print(soup.title)
print(soup.title.name)
print(soup.title.string)
print(soup.p)
print(soup.a)
print("*" * 50)

# 获取标签属性值
print(soup.p["class"])
print("*" * 50)
for data in soup.find_all("a", class_="sister"):
    print(data.get("href")) # 获取属性值
    print(data.get_text())  # 获取文本内容

print("*" * 50)
# 根据属性值查找
print(soup.find("a", id="link3"))
print("*" * 50)

print(soup.find_all("a"))  # 返回的结果是列表
print(soup.find_all("a", class_="sister"))  # 根据class定位，需要在class后面加上_
print("*" * 50)


print(soup.body.p)
print(soup.find_all(["a", "p"]))
print("*" * 50)

print(soup.select("a", class_="sister"))
# 找第三个a标签
print(soup.select("a:nth-of-type(3)"))