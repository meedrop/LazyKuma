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

# 登入时跳转到dashboard
@app.route('/',methods=['GET','POST'])
@login_require.require
def go_2_dashboard():
    return redirect('/dashboard/show')

# 个人中心页面
@app.route('/user/userinfo',methods=['GET','POST'])
#@app.route('/index')
@login_require.require
def userinfo():   # 该模块获取用户全局信息 保证个人中心展示
    if request.method == "GET":
        name = session.get('name')
        where = {'name':name}
        fields = ['id','name','name_cn','email','mobile','role']
        content = DB().check(db_table,fields,where)
        user = dict((k,content[i]) for i,k in enumerate(fields))
        print user
        return render_template("userinfo.html",user=user)

# 用户登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":         # 页面输入账号密码后post请求进行处理
        user = dict((k,v[0]) for k,v in dict(request.form).items())
        user['password'] = hashlib.md5(user['password']+salt).hexdigest()   # 密码进行加密存储数据库，解密时也一样
        where = {'name':user['username']}
        fields = ['name','password','role','status']
        # 传给数据库类处理
        content = DB().check(db_table,fields,where)
        '''
        数据库fetch出来的结果就像这('jack','123456','admin','1'),要准确拿出对应的值，可用下面这个方法
        user={}
        for i,k in enumerate(fields):
            result[i]=user[k]
        得到user={'name':'jack','passowrd':'1','status':'1','role':'admin'}
        '''
        if not content:
            error = "用户名不存在"
            return json.dumps({'code':1,'error':error}) # 返回code及error信息给前端jquery判断处理
        result = dict((k,content[i]) for i,k in enumerate(fields))
        if result['password'] != user['password']:
            error = "密码错误"
            return json.dumps({'code':1,'error':error})
        if result['status'] == 1:
            error = "账户被锁定"
            return json.dumps({'code':1,'error':error})
        session['name'] = result['name']    # 密码验证通过为用户增加session
        session['role'] = result['role']    # 获取全局的用户权限
        info = "登录成功"
        return json.dumps({'code':0,'info':info})
    if request.method == "GET":
        return render_template('login.html')  # 第一次打开页面为GET请求，返回一个空登录页面

# 更新个人信息
@app.route('/user/update',methods=['GET','POST'])
@login_require.require
def user_update():
    if request.method == "POST": # 接收前端修改信息的post请求
        user = dict((k,v[0]) for k,v in dict(request.form).items())
        where = {'id':user['id']}
        #fields = ['name_cn','email','mobile','role']
        content = DB().update(db_table,user,where)
        if content == 0:
            return json.dumps({'code':0,'info':'更新成功'})
        else:
            return json.dumps({'code':1,'error':'更新错误'})
    if request.method == "GET":  # 更新信息栏 GET请求时,返回用户的信息进行渲染
        id = request.args.get('id')
        where = {'id':id}
        fields = ['id','name','name_cn','email','mobile','role','status']
        content = DB().check(db_table,fields,where)
        user = dict((k,content[i]) for i,k in enumerate(fields))
        print user
        return json.dumps(user)

# 个人中心页面更新密码
@app.route('/user/updateOnepwd',methods=['GET','POST'])
@login_require.require
def user_updateOnepwd():
    if request.method == "POST":
        pwds = dict((k,v[0]) for k,v in dict(request.form).items())
        fields = ['password']
        where = {'id':pwds['id']}
        content1 = DB().check(db_table,fields,where)
        result = dict((k,content1[i]) for i,k in enumerate(fields))
        pwds['oldpwd'] = hashlib.md5(pwds['oldpwd']+salt).hexdigest()
        if pwds['oldpwd'] != result['password']: # 旧密码匹配
            return json.dumps({'code':1,'error':'旧密码不正确'})
        elif pwds['newpwd'] != pwds['ackpwd']: # 新密码匹配
            return json.dumps({'code':1,'error':'确认密码不一致'})
        else:
            newpwd = {'password':hashlib.md5(pwds['newpwd']+salt).hexdigest()}
            content2 = DB().update(db_table,newpwd,where)
            if content2 == 0:
                return json.dumps({'code':0,'info':'更新成功'})
            else:
                return json.dumps({'code':1,'error':'更新错误'})

# 用户列表页面
@app.route('/user/userlist',methods=['GET','POST'])
@login_require.require
def user_userlist():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        fields = ['id','name','name_cn','email','mobile','role','status']
        res = DB().select_NoWhere(db_table,fields)
        '''
        res的格式如下:((1,jack,杰克,xxx@qq.com,123333,common),(2,mary,玛丽,xxx@qq.com,123333,common),...)
        需要转换为格式:[{"id":123,"name":"jack"...},{"id":123,"name":"mary"...}]
        便于页面for循环渲染
        '''
        users = []
        for content in res:
            tmp = dict((k,content[i]) for i,k in enumerate(fields))
            users.append(tmp)
        # 获取所有用户信息后 在页面展示
        return render_template('userlist.html',users=users)

# 删除用户
@app.route('/user/delete',methods=['GET','POST'])
@login_require.require
def delete_user():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        id = request.args.get('id')
        where = {"id":id}
        print where
        content = DB().delete(db_table,where)
        if content == 0:
            return json.dumps({'code':0,'info':'删除成功'})
        else:
            return json.dumps({'code':1,'error':'删除失败'})

# 添加用户
@app.route('/user/add',methods=['GET','POST'])
@login_require.require
def add_uer():
    if session["role"] != "admin":
        return redirect('/')
    if request.method == "GET":
        return render_template("adduser.html")
    if request.method == "POST":
        user = dict((k,v[0]) for k,v in dict(request.form).items())
        user['password'] = hashlib.md5(user['password']+salt).hexdigest()
        fields = ['name','name_cn','password','email','mobile','role','status']
        content = DB().insert(db_table,fields,user)
        if content == 0:
            return json.dumps({'code':0,'info':'添加成功'})
        else:
            return json.dumps({'code':1,'error':'添加失败'})

# 退出登录
@app.route('/user/logout',methods=['GET','POST'])
def logout():
    if session['name'] or session['role']:
        session.pop('name',None)
        session.pop('role',None)
    return redirect('/login')

#oldpwd,newpwd,ackpwd




# 访问login的时候，如果有session就跳到个人中心界面，没有就提示登录
# 增加账户锁定功能
