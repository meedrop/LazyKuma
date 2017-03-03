#!/usr/bin/env python
# coding:utf-8

from flask import Flask
import sys
# reload(sys)
# sys.setdefaultencoding('utf8') # 程序内部有中文参数，gunicorn直接调用

app = Flask(__name__)
app.secret_key = 'as$11#@!f3sf23a'

import user
import server
import dashboard