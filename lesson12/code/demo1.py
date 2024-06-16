# -*- coding:utf-8 -*-
import re
var = r"你好，我是坤哥，我喜欢打篮球，你好呀\n"
# match：从头匹配，只匹配一个结果，如果开头不是，则返回None
r1 = re.match(r"你好", var)

# search：从开头匹配，只要匹配到符合规则的数据，则返回
r2 = re.search(r"坤哥", var).group()
# r2 = re.search(r"\\n", var)
# print(r2)

"""
match与search
相同点: 只返回一个匹配结果
不通电: match开头没有，则返回None；search只要字符串当中有符合的，则返回
"""

# findall 只要是符合匹配规则的数据，全部都会拿到，并且返回一个列表
r3 = re.findall(r"你好", var)

# compile：实现更高效的匹配
r4 = re.compile(r"坤哥")
r5 = r4.search(var)

# split：切割字符串
var2 = "你好|坤哥|我爱篮球|鸡你太美"
# print(var2)
r6 = re.split(r"\|",var2, maxsplit=2)

# sub：
r7 = re.sub(r"坤哥","只因哥",var2)
print(r7)
