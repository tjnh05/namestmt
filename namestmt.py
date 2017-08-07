# coding=utf-8
#
#test if name is good.
#programmed by Bodhi Wang
#bodwang@deloitte.com.cn
#2017.8.4
'''
formart of result, for example:

[{'姓': '唐'},
 {'性别': '男'},
 {'生日': '201701230327'},
 [{'五格数理': 83,
   '八字五行': 95,
   '八字喜用神': '水',
   '名': '梓渝',
   '名字综合评分': 91,
   '周易卦象': 95,
   '推荐': '是',
   '数理分析': '天格11解析\n'
           '（旱苗逢雨）万物更新，调顺发达，恢弘泽世，繁荣富贵。\n'
           '地格24解析\n'
           '（掘藏得金）家门余庆，金钱丰盈，白手成家，财源广进。\n'
           '人格21解析\n'
           '（明月中天）光风霁月，万物确立，官运亨通，大搏名利。\n'
           '外格14解析\n'
           '（破兆） 家庭缘薄，孤独遭难，谋事不达，悲惨不测。\n'
           '总格34解析\n'
           '（破家） 破家之身，见识短小，辛苦遭逢，灾祸至极。\n'
           '三才解析\n'
           '成功顺调,无障碍而向上发展,基础境遇也得安泰,终生享受幸福繁荣长寿的吉配。\n'
           '基础运解析\n'
           '吉祥安泰\n'
           '成功运解析\n'
           '同为木,相辅相成,成功顺利,能平安实现自己的目的。\n'
           '人际关系解析\n'
           '性格稳健,善忍耐,温良亲切,礼貌周到,慷慨好施。易患皮肤病,中风中邪、感冒等。三才良善者,可望平安。\n'
           '性格影响解析\n'
           '性情多好静,富于理智。温厚中带有华丽气质具有不屈不挠的精神。...',
   '生肖吉凶': 100,
   '音形义': 86}]]
'''
from urllib import parse
from bs4 import BeautifulSoup
from pprint import pprint
import requests
#import io
#import time
#import sys
import re


class NamEstmt:
   #detail score types
   scoreTypes = {
      0:"音形义",
      1:"八字五行",
      2:"生肖吉凶",
      3:"五格数理",
      4:"周易卦象",
   }

   def __init__(self, 
                surname,    # last name, 姓
                name,       # first name, 名
                gender,     # 性别, 男/女
                birthdaytm  # 出生时间，格式:YYYYMMDD24HMI,如：201701012110
                ):
      self.surname = surname
      self.name = name
      self.gender = gender
      self.birthdaytm = birthdaytm

      self.last_name = surname
      self.first_names = []

      if isinstance(name,list):
         self.first_names = name
      elif isinstance(name,str):
         self.first_names.append(name)
      elif isinstance(name,set) or isinstance(first_name,tuple):
         self.first_names = list(name)

      self.sex = "1" if gender in ("男","1","male","Male") else "2"
      self.year = birthdaytm[0:4]
      self.month = birthdaytm[4:6]
      self.day = birthdaytm[6:8]
      self.hour = birthdaytm[8:10]
      self.minute = birthdaytm[10:12]

      #make cookies
      self.cookies={
         "qmyw11flag":"1",       #FLAG
         "qmyw11xing":self.last_name,#LAST_NAME
         "qmyw11xingbie":self.sex,    #SEX
         "qmyw11nian":self.year,      #YEAR
         "qmyw11yue":self.month,      #MONTH
         "qmyw11ri":self.day,         #DAY
         "qmyw11shi":self.hour,       #HOUR
         "qmyw11fen":self.minute,     #MINUTE
         "qmyw11zwy":"mm",       #LZYZ
         "qmyw11zhuangongli":"0",#ZHUANGONGLI
         "qmyw11zhentaiyang":"0",#ZHENTAIYANG
         "qmyw11qim":"zhqm",     #QIM
      }

      #make url parameters
      self.params={
         "xing":self.last_name,  #last name
         "ming":"",              #first name
      }

      self.RKMNT_LIST=list()
      self.result=list()
      self.result.append({"姓":surname})
      self.result.append({"性别":gender})
      self.result.append({"生日":birthdaytm})

      self.regex = re.compile(r"[\r\n\t\u3000]+")
      self.homeurl = "https://qiming.yw11.com/newqiming/qm/cm/"
       

   def makecookies(self, pcookies=None):
      lcookies = pcookies

      #add cookies to query
      for item in self.cookies.keys():
         value = self.cookies[item]
         if item == "qmyw11xing":
            value = parse.quote(self.cookies[item])
         lcookies.set(item,value)

      return lcookies

   def setming(self, lastname):
      self.params["ming"] = lastname 

   def estimate(self, 
                scorelimit=90, # 综合评分推荐阈值，缺省90
                debug=0    # 调试选项，缺省为0。如果为1或2,则打印相应级别跟踪信息
               ):
      check_lists=list()
      for name in self.first_names:
         #request home url for query and retrieve basic cookies
         session = requests.Session()
         try:
            r = session.get(self.homeurl)
         except (HTTPError, URLError) as e:
            if debug >0:
               print(e)
            continue

         #add cookies to query
         mycookies = self.makecookies(pcookies=r.cookies)

         if debug >0:
            print("name:"+name)
         self.setming(lastname=name)

         check_list=dict()
         check_list["名"]=name

         #make query url and perform request and parse
         dlurl = self.homeurl+"zhfx?"+parse.urlencode(self.params)
         #print("dlurl="+dlurl)
         try:
            r = session.get(dlurl, cookies=mycookies)
         except (HTTPError, URLError) as e:
            if debug >0:
               print(e)
            continue
   
         #pprint(r.text)
         if debug > 1:
            print("状态码:"+ str(r.status_code) + " - "+str(r.ok))

         bsObj = BeautifulSoup(r.text,"lxml")

         #综合评分
         tot_score = 0
         try:
            zhpf = bsObj.find("span",{"class":"num"})
            tot_score = int(zhpf.get_text().strip())
         except AttributeError as e:
            if debug > 0:
               print("Name %s not processed!" % name)
               print(e)
            continue
         check_list["名字综合评分"]=tot_score

         #明细项评分
         try:
            dtl_scores = bsObj.findAll("span",{"class":"co1 bd"})
            for typeid in range(5):
               check_list[self.scoreTypes[typeid]]=int(dtl_scores[typeid].get_text().strip())
         except AttributeError as e:
            if debug >0: 
               print("Tag <span>-<class>-<col bd> was not found")
               print(e)
            continue
   
         #八字喜用神
         try:
            bzxys = bsObj.find("span",{"class":"co1 bd f24"})
            check_list["八字喜用神"]=bzxys.get_text().strip()
         except AttributeError as e:
            if debug >0:
               print("Tag <span>-<class>-<col bd f24> was not found")
               print(e)
            continue
   
         #八字喜用神
         slfxlist=[]
         try:
            for sibling in bsObj.find("table",
                           {"id":"wgsc"}).tr.next_sibling.next_sibling.next_siblings:
               if sibling.name != "tr":
                  continue
               for child in sibling.children:
                  if child.name !="td" or child.get_text()=='\xa0':
                     continue
                  #print(regex.sub("",child.get_text()))
                  slfxlist.append(self.regex.sub("",child.get_text()))
         except AttributeError as e:
            if debug > 0:
               print("Tag <table>-<id>-<wgsc> was not found")
               print(e)
         check_list["数理分析"]="\n".join(slfxlist)
         if debug > 1:
            pprint(check_list["数理分析"])

         #是否推荐
         if tot_score >= scorelimit:
            check_list["推荐"]="是"
            self.RKMNT_LIST.append({name:tot_score})
         else:
            check_list["推荐"]="否"

         check_lists.append(check_list)
      
      #更新result值
      self.result.append(check_lists)

      return self.result
