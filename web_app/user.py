#!/usr/bin/env python
# coding:utf-8

from web_app import app
from flask import Flask,request,render_template,redirect,session
from tools import login_require,logstdout
import datetime,json
import hashlib
from dbtool import DB

salt = "$z%5^u3I"
logs = logstdout.WriteLog('mylog')
db_table = 'Users'
# 个人中心页面
@app.route('/')
@app.route('/index')
@login_require.require
def index():
    logs = logstdout.WriteLog('mylog')
    logs.info("this is a test")
    return "this is test"

# 用户登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":          # 页面输入账号密码后post请求进行处理
        user = dict((k,v[0]) for k,v in dict(request.form).items())
        user['password'] = hashlib.md5(user['password']+salt).hexdigest() # 密码进行加密存储数据库，解密时也一样
        where = {'name':user['username']}
        fields = ['name','password','role','status']
        # 传给数据库类处理
        content = DB().check(db_table,fields,where)
        '''
        数据库fetch出来的结果就像这('jack','123456','admin','1'),要准确拿出对应的值，可用下面这个方法
        user={}
        for i,k in enumerate(fields):
            result[i]=user[k]
        '''
        result = dict((k,content[i]) for i,k in enumerate(fields))
        if not result:
            error = "username not exist!"
            return json.dumps({'code':1,'error':error}) # 返回code及error信息给前端jquery判断处理
        if result['password'] != user['password']:
            error = "password not right!"
            return json.dumps({'code':1,'error':error})
        if result['status'] == 1:
            error = "account locked!"
            return json.dumps({'code':1,'error':error})
        # 密码验证通过为用户增加session
        session['name'] = result['name']
        session['role'] = result['role']
        sucess = "login successful!"
        return json.dumps({'code':0,'sucess':sucess})
    if request.method == "GET":
        return render_template('login.html')  # 第一次打开页面为GET请求，返回一个空登录页面


# 访问login的时候，如果有session就跳到个人中心界面，没有就提示登录