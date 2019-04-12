# supervisor_openstack
一个用于监控OpenStack虚拟机，前期提供监测CPU、内存、网口和磁盘等，使用libvirt获取相关信息，使用flask和ajax 和boostrap构建实时监控
####
####
<h4>1.libvart<h4></br>
    <p>使用libvirt对OpenStack虚拟机进行相关数据采集，并存储到mongodb数据库中</p></br>
<h4>2.flask+boostrap3+ajax<h4></br>
     <p>实现数据的实时监控和异步更新</p></br>
<h4>3.告警<h4></br>
<p>添加邮箱，CPU告警信息邮箱通知</p></br>
<h4>4.提供OpenStack安装PPT文档<h4></br>


<h4>###注意：<h4></br>
<p>1. pymongo安装版本 <=3.0 建议 pip install pymongo==2.8###</p></br>
         <p>2. python2.7 由于libvart对python3.0以上支持不好，故用python2.7版本</p></br>
#####

###

       
###
<p>该项目适合新手学习和交流，如果有任何问题请联系我Email: lizhipengqilu@gmail.com</p></br>
<p>同时希望大家提出宝贵意见，欢迎学习交流，如果你喜欢该项目，请收藏或者fork一下，你的主动将是我前行的动力</p></br>
###
<h4>项目预览<h4></br>
###
<p>![Image text](https://github.com/Frank-qlu/supervisor_openstack/tree/master/images/cpu.png)</p></br>
<p>![Image text](https://github.com/Frank-qlu/supervisor_openstack/tree/master/images/memory.png)</p></br>
<p>![Image text](https://github.com/Frank-qlu/supervisor_openstack/tree/master/images/disk.png)</p></br>
<p>![Image text](https://github.com/Frank-qlu/supervisor_openstack/tree/master/images/disk.png)</p></br>
<p>![Image text](https://github.com/Frank-qlu/supervisor_openstack/tree/master/images/warning.png)</p></br>
