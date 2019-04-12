#author：(李志鹏)Frank Lee
#2019 年4 月12日
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,render_template,g
# import sql
# import main1
import test
app=Flask(__name__)
import mail

# main1.main()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cpu/")
def CPU():
    ones = [[i["current_time"] , i["cpu_usage"]] for i in test.collection.find()]
    # for x in test.collection.find():
    #     print  x["cpu_usage"]
    # print (test.collection.find_one())
    g.data=ones
    # print g.data
    g.len1=len(g.data)
    # for i in  range(g.l):
    #   print g.data[i][1]
    li = []
    for i in range(g.len1):
        li.append(g.data[i][1])
    g.li = li
    # print g.li
    return render_template("cpu.html")
@app.route("/memory/")
def Memory():
    ones = [[i["current_time"] , i["memory_used"]] for i in test.collection.find()]
    # for x in test.collection.find():
    #     print  x["cpu_usage"]
    # print (test.collection.find_one())
    g.memory=ones
    # print g.data
    g.len_memory=len(g.memory)
    # for i in  range(g.l):
    #   print g.data[i][1]
    return render_template("memory.html")
@app.route("/disk/")
def disk():
    ones = [[i["current_time"] , i["disks"][0]['disk_read']] for i in test.collection.find()]
    # for x in test.collection.find():
    #     print  x["cpu_usage"]
    # print (test.collection.find_one())
    g.disk=ones
    # print g.data
    g.len_disk=len(g.disk)
    # for i in  range(g.l):
    #   print g.data[i][1]
    return render_template("disk.html")
@app.route("/network/")
def Network():
    ones = [[i["current_time"] , i["nics"][0]["net_receive_write"]] for i in test.collection.find()]
    # for x in test.collection.find():
    #     print  x["cpu_usage"]
    # print (test.collection.find_one())
    print ones
    g.network=ones
    # print g.data
    g.len_network=len(g.network)

    return render_template("network.html")


if __name__ == '__main__':
    app.run(debug=True,host="192.168.104.10")
