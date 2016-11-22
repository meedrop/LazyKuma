#!/usr/bin/env python
# coding:utf-8

from web_app import app
from flask import Flask,render_template,redirect,session
from tools import login_require,logstdout


@app.route('/')
@app.route('/index')
#@login_require.require
def index():
    logs = logstdout.WriteLog('mylog')
    logs.info("this is a test")
    return "this is test"
