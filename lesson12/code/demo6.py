# -*- coding:utf-8 -*-
import re

var = "123456789"
r1 = re.search(r"\d{3}", var).group()

r2 = re.search(r"\d{2,}", var).group()

r3 = re.search(r"\d{2,5}", var).group()

# 匹配座机号码
# 123-45678
var2 = "023-33061"
r4 = re.search(r"\d{3}-\d{5,6}", var2).group()
print(r4)



