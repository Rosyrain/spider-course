# -*- coding:utf-8 -*-
import re

var1 = "全民制作人大家好，我是练习时长两年半的偶像练习生"

r1 = re.search(r"全民制作人.", var1).group()

r2 = re.search(r"制作1人|练习生", var1).group()

var2 = "变形金刚1,变形金刚2,变形金刚3,变形金刚4,变形金刚5,变形金刚6"

r3 = re.findall(r"变形金刚[123]", var2)

r4 = re.findall(r"变形金刚[^123]", var2)

var3 = "123456abcvdefgABVCDFTHFI029876589543"

r5 = re.findall(r"[a-z]", var3, re.I)

var4 = "你好."

r6 = re.search(r"\.", var4).group()



