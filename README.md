# 基于Flask+Bootstrap构建的运维平台 
## 1. 介绍
目前主要做了用户管理系统，资产管理系统，监控报表展示，zabbix二次开发等功能，其他功能逐渐添加。
前端使用了`html`、`bootstrap`模板及`jquery`插件，绘图则通过`Echarts`实现。
后端使用`Flask`处理`http`请求，`python`进行逻辑处理，对`mysql`进行增删查改操作。
zabbix展示使用restful api获取监控数据实时展示

对于功能设计可以参考`LazyKuma.xmind`脑图。

## 2. 运行环境的准备
* `python2.7` 平台

运行如下命令安装环境
* `pip install flask`
* `pip install DBUtils`
* `yum instll mysql-devel`
* `yum install python-devel`
* `pip install MySQL-python`

## 3. 数据库配置
* 数据库的配置文件在`conf/config.py`根据你的环境相应修改即可。
* 提供了2个sql文件,分别是`LazyKuma.sql`,`LazyKuma_data.sql`,一个是不带表数据，另外一个带表数据，建议运行第二个sql脚本，初始化后使用用户`William/123`可登入。


## 4. zabbix配置
* 安装`zabbix 3.0`,其他版本也可以，未做试验
* `conf/config.py`根据你的环境相应修改
* zabbix控制台中，你还要提供一个主机名为`Zabbix server`的host主机
* 默认只做了`system.cpu.util[,idle]`这个key的数据展示
* 展示界面设置了30秒获取一次数据，观察时请耐心等待一下

## 5. 运行起来
```
# python run.py

```

## 4. 访问实例
通过`http://ip:9999`访问登录即可
下面是一些页面示例：


* 展示界面
![](http://ofus5xwey.bkt.clouddn.com/lazy1.png)
* 用户界面
![](http://ofus5xwey.bkt.clouddn.com/lazy_2.png)
* 资产界面1
![](http://ofus5xwey.bkt.clouddn.com/lazy_3.png)
* zabbix监控界面
![](http://ofus5xwey.bkt.clouddn.com/lazy5.png)
