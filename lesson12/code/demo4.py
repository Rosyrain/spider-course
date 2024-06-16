# -*- coding:utf-8 -*-
import re

var1 = "1234556789love1234567"

r1 = re.findall(r"[0-9]", var1)
r2 = re.findall(r"\d", var1)

r3 = re.findall(r"[^0-9]", var1)
r4 = re.findall(r"\D", var1)


var2 = "12345_love_6789_坤哥爱篮球_RAP"
r5 = re.findall(r"[a-zA-Z0-9_]", var2)
r6 = re.findall(r"\w", var2, re.A)


r7 = re.findall(r"[^a-zA-Z0-9_]", var2)
r8 = re.findall(r"\W", var2, re.A)

var3 = "你好   我是IKUN"

r9 = re.findall(r"\s", var3)
r10 = re.findall(r"\S", var3)
print(r9)
print(r10)
