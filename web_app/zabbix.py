#!/usr/bin/env python
# coding:utf-8

from web_app import app
from flask import Flask,request,render_template,redirect,session
from tools import login_require,logstdout
import datetime,json
import hashlib
import time
from zabbix_tool import zabbix

logs = logstdout.WriteLog('mylog')
hosts = "Zabbix server"
key = "system.cpu.util[,idle]"

# 展示图标页面
@app.route('/zabbix/monitor',methods=['GET','POST'])
@login_require.require
def zabbix_monitor():
    if request.method == "GET":
        return render_template("monitor/zabbix.html")

# 获取数据
@app.route('/zabbix/data',methods=['GET','POST'])
# @app.route('/zabbix/monitor',methods=['GET','POST'])
@login_require.require
def zabbix_data():
    if request.method == "GET":
        hostids = zabbix().host_get(hosts)[0]["hostid"]
        itemid = zabbix().item_get(hostids,key)[0]["itemid"]
        onehour_before = int(time.time()-3600) # 设置获取监控数据时间为1小时
        now = int(time.time())
        data = zabbix().history_get(itemid,onehour_before,now)
        for i in data:
            # 传过来的data是时间戳,转换成00:00的格式给前端页面
            t = int(i['clock'])
            local = time.localtime(t)
            HM = time.strftime("%H:%M",local)
            ymd = time.strftime("%Y-%m-%d",local)
            i['clock'] = HM
            i['day'] = ymd
        return json.dumps(data)



















