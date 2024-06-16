# -*- coding:utf-8 -*-
import re

var1 = r"你好\n坤哥,我的资产100000$"

r1 = re.search(r"\\n", var1).group()

r2 = re.search(r"\$" ,var1).group()
print(r2)
