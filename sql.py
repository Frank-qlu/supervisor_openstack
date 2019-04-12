#author：(李志鹏)Frank Lee
#2019 年4 月12日

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymongo
#连接mongodb
client = pymongo.MongoClient('mongodb://localhost:27017/')
#指定数据库
db = client.monitor
#指定集合
collection = db.domain#数据
