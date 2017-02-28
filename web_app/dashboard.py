#!/usr/bin/env python
# coding:utf-8

from web_app import app
from flask import Flask,request,render_template,redirect,session
from tools import login_require,logstdout
import datetime,json
import hashlib
from dbtool import DB

logs = logstdout.WriteLog('mylog')

# 个人中心页面
@app.route('/dashboard/show',methods=['GET','POST'])
@login_require.require
def show():   # 该获取全局信息进行页面展示
    if request.method == "GET":
        info = {}
        # 获取用户总数
        info['userSum'] = DB().select_NoWhere("Users",["count(*)"])[0][0]
        logs.info("获取用户总数为:%s" % (info['userSum']))
        # 获取设备总数
        info['serverSum'] = DB().select_NoWhere("Servers_Info",["count(*)"])[0][0]
        logs.info("获取设备总数为:%s" % (info['serverSum']))
        # 获取运行状态服务器总数
        info['serverRunning'] = DB().check("Servers_Status",["count(*)"],{"status":0})[0] # 注意不带where和带whereselect出来结果不一样
        logs.info("获取运行中设备总数为:%s" % (info['serverRunning']))
        # 获取关机状态
        info['serverDown'] = DB().check("Servers_Status",["count(*)"],{"status":1})[0]
        logs.info("获取运行中设备总数为:%s" % (info['serverDown']))
        return render_template("/dashboard/dashboard.html",info=info)

'''
# 用户列表页面
@app.route('/user/userlist',methods=['GET','POST'])
@login_require.require
def user_userlist():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        fields = ['id','name','name_cn','email','mobile','role','status']
        res = DB().select_NoWhere(db_table,fields)

        users = []
        for content in res:
            tmp = dict((k,content[i]) for i,k in enumerate(fields))
            users.append(tmp)
        # 获取所有用户信息后 在页面展示
        return render_template('userlist.html',users=users)

        tuple_sid = DB().check(server_info_table,['sid'],{'sn':servers['sn']})
'''