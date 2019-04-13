<h1>#supervisor_openstack</h1>
<h2>一个用于监控OpenStack虚拟机，前期提供监测CPU、内存、网口和磁盘等，使用libvirt获取相关信息，使用flask和ajax 和boostrap构建实时监控</h2>
####
####
<h4>1.libvirt<h4></br>
    <p>使用libvirt对OpenStack虚拟机进行相关数据采集，并存储到mongodb数据库中</p></br>
<h4>2.flask+boostrap3+ajax<h4></br>
     <p>实现数据的实时监控和异步更新</p></br>
<h4>3.告警<h4></br>
<p>添加邮箱，CPU告警信息邮箱通知</p></br>
<h4>4.提供OpenStack安装PPT文档<h4></br>


<h4>###注意ﺿh4></br>
<p>1. pymongo安装版本 <=3.0 建议 pip install pymongo==2.8###</p></br>
         <p>2. python2.7 由于libvart对python3.0以上支持不好，故用python2.7版本</p></br>
#####

###

       
###
<p>该项目适合新手学习和交流，如果有任何问题请联系我Email: lizhipengqilu@gmail.com</p></br>
<p>同时希望大家提出宝贵意见，欢迎学习交流，如果你喜欢该项目，请收藏或者fork一下，你的主动将是我前行的动力</p></br>
<p>###项目预览###<p></br></br>
<img src="https://raw.githubusercontent.com/Frank-qlu/supervisor_openstack/master/images/1.png">
<img src="https://raw.githubusercontent.com/Frank-qlu/supervisor_openstack/master/images/2.png">
<img src="https://raw.githubusercontent.com/Frank-qlu/supervisor_openstack/master/images/3.png">
<img src="https://raw.githubusercontent.com/Frank-qlu/supervisor_openstack/master/images/4.png">
<img src="https://raw.githubusercontent.com/Frank-qlu/supervisor_openstack/master/images/5.png">