# -*- coding:utf-8 -*-
import re

var1 = "全民制作人大家好，我是练习时长两年半的偶像练习生"
r1 = re.search(r".*", var1).group()

var2 = "zaooooo"
r2 = re.search(r"zo+", var2)

var3 = "lobaobao"
r3 = re.search(r"lo(ve)?", var3).group()
print(r3)