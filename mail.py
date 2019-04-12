#author：(李志鹏)Frank Lee
#2019 年4 月12日

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import yagmail
import pymongo
#连接mongodb
client = pymongo.MongoClient('mongodb://localhost:27017/')
#指定数据库
db = client.monitor
#指定集合
collection = db.domain#数据
#remind
# 登录你的邮箱
yag = yagmail.SMTP(user='your mail', password='your mail password', host='smtp.qq.com')
ones = [[i["current_time"] , i["cpu_usage"]] for i in collection.find()]
li = []
for i in range(len(ones)):
    li.append(ones[i][1])
# print range(len(li))
for aaa in range(len(li)):
    # print aaa
    # print li[aaa]
    # print type(float(li[aaa]))
    if  float(li[aaa])> 90:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!"
        # 发送邮件
        yag.send(to=['your mail which you want send to'], subject='cpu告警',
                     contents=['你的cpu告警啦'])