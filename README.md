# supervisor_openstack
一个用于监控OpenStack虚拟机，前期提供监测CPU、内存、网口和磁盘等，使用libvirt获取相关信息，使用flask和ajax 和boostrap构建实时监控
####
####
1.libvart
    使用libvirt对OpenStack虚拟机进行相关数据采集，并存储到mongodb数据库中
2.flask+boostrap3+ajax
     实现数据的实时监控和异步更新
3. 告警
 添加邮箱，CPU告警信息邮箱通知

4. 提供OpenStack安装PPT文档


###注意：1. pymongo安装版本 <=3.0 建议 pip install pymongo==2.8###
         2. python2.7 由于libvart对python3.0以上支持不好，故用python2.7版本
#####

###

       
###
该项目适合新手学习和交流，如果有任何问题请联系我Email: lizhipengqilu@gmail.com
同时希望大家提出宝贵意见，欢迎学习交流，如果你喜欢该项目，请收藏或者fork一下，你的主动将是我前行的动力
###
项目预览
###
![Image text](https://github.com/Frank-qlu/recruit/blob/master/%E6%8B%9B%E8%81%98%E7%88%AC%E8%99%AB/images/1.png)
![Image text](https://github.com/Frank-qlu/recruit/blob/master/%E6%8B%9B%E8%81%98%E7%88%AC%E8%99%AB/images/2.png)
![Image text](https://github.com/Frank-qlu/recruit/blob/master/%E6%8B%9B%E8%81%98%E7%88%AC%E8%99%AB/images/wordcount.png)
![Image text](https://github.com/Frank-qlu/recruit/blob/master/%E6%8B%9B%E8%81%98%E7%88%AC%E8%99%AB/images/educate.png)
![Image text](https://github.com/Frank-qlu/recruit/blob/master/%E6%8B%9B%E8%81%98%E7%88%AC%E8%99%AB/images/experience.png)
![Image text](https://github.com/Frank-qlu/recruit/blob/master/%E6%8B%9B%E8%81%98%E7%88%AC%E8%99%AB/images/search.png)