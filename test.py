#! /usr/bin/env python3.5
# coding=utf-8
#
#test if name is good.
#programmed by Bodhi Wang
#bodwang@deloitte.com.cn
#2017.8.7
from pprint import pprint
import namestmt


#just for test
nmestmt = namestmt.NamEstmt(surname="唐",
                   name=["梓渝",],
                   gender="男",
                   birthdaytm="201701230327"
                  )
nmestmt.estimate(
                scorelimit=90, # 综合评分推荐阈值，缺省90
                debug=1    # 调试选项
               )
#输出结果
print("\n名字分析：")
pprint(nmestmt.result)
print("\n推荐列表：")
pprint(nmestmt.RKMNT_LIST)
#print("\n")
#pprint(nmestmt.result[3][0])
