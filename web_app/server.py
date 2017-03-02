#!/usr/bin/env python
# coding:utf-8

from web_app import app
from flask import Flask,request,render_template,redirect,session
from tools import login_require,logstdout
import datetime,json
import hashlib
from dbtool import DB

logs = logstdout.WriteLog('mylog')
server_info_table = 'Servers_Info'
server_status_table = 'Servers_Status'

# 添加设备信息
@app.route('/server/add',methods=['GET','POST'])
@login_require.require
def add_server():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        return render_template("/server/addserver.html")
    if request.method == "POST":
        servers = dict((k,v[0]) for k,v in dict(request.form).items()) # 获取到所有post数据分2张表插入,表外键关联
        logs.info("获取添加设备数据:%s" % (servers))
        fields1 = ['machine_room','cabinet','sn','server_type','configuration'] # 插入第一张表
        content1 = DB().insert(server_info_table,fields1,servers)
        # 获取外键sid插入第二张表
        tuple_sid = DB().check(server_info_table,['sid'],{'sn':servers['sn']})
        servers['sid'] = tuple_sid[0]
        fields2 = ['sid','server_name','status','ip','services']
        content2 = DB().insert(server_status_table,fields2,servers)
        if content1 == 0 and content2 == 0:
            return json.dumps({'code':0,'info':'添加成功'})
        else:
            return json.dumps({'code':1,'error':'添加失败'})

# 添加设备状态
@app.route('/server/add',methods=['GET','POST'])
@login_require.require
def add_server():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        res = DB().select_NoWhere(server_info_table,"*")
        sids = []
        for content in res:
            tmp = dict((k,content[i]) for i,k in enumerate(fields))
            sids.append(tmp)
        return render_template("/server/addserver_status.html")


# 设备信息列表页面
@app.route('/server/list',methods=['GET','POST'])
@login_require.require
def server_list():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        fields = ['sid','machine_room','cabinet','sn','server_type','configuration']
        res = DB().select_NoWhere(server_info_table,fields)
        servers = []
        for content in res:
            tmp = dict((k,content[i]) for i,k in enumerate(fields))
            servers.append(tmp)
        # 获取所有用户信息后 在页面展示
        return render_template("/server/serverlist.html",servers=servers)

# 设备状态列表页面
@app.route('/server/liststatus',methods=['GET','POST'])
@login_require.require
def server_liststatus():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        fields = ['sid','server_name','status','ip','services']
        res = DB().select_NoWhere(server_status_table,fields)
        servers = []
        for content in res:
            tmp = dict((k,content[i]) for i,k in enumerate(fields))
            servers.append(tmp)
        # 获取所有用户信息后 在页面展示
        return render_template("/server/serverlist_status.html",servers=servers)

# 删除设备信息
@app.route('/server/delete',methods=['GET','POST'])
@login_require.require
def delete_serverInfo():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        id = request.args.get('id')
        where = {"sid":id}
        print where
        content = DB().delete(server_info_table,where)
        if content == 0:
            return json.dumps({'code':0,'info':'删除成功'})
        else:
            return json.dumps({'code':1,'error':'删除失败'})

# 删除设备状态
@app.route('/server/deleteStatus',methods=['GET','POST'])
@login_require.require
def delete_serverStatus():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        id = request.args.get('id')
        where = {"sid":id}
        print where
        content = DB().delete(server_status_table,where)
        if content == 0:
            return json.dumps({'code':0,'info':'删除成功'})
        else:
            return json.dumps({'code':1,'error':'删除失败'})

# 更新设备信息
@app.route('/server/updateInfo',methods=['GET','POST'])
@login_require.require
def server_updateInfo():
    if request.method == "POST": # 接收前端修改信息的post请求
        server = dict((k,v[0]) for k,v in dict(request.form).items())
        where = {'sid':server['sid']}
        content = DB().update(server_info_table,server,where)
        if content == 0:
            return json.dumps({'code':0,'info':'更新成功'})
        else:
            return json.dumps({'code':1,'error':'更新错误'})
    if request.method == "GET":  # 更新信息栏 GET请求时,返回用户的信息进行渲染
        id = request.args.get('id')
        where = {'sid':id}
        fields = ['sid','machine_room','cabinet','sn','server_type','configuration']
        content = DB().check(server_info_table,fields,where)
        server = dict((k,content[i]) for i,k in enumerate(fields))
        print server
        return json.dumps(server)
