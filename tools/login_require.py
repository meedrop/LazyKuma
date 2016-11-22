#!/usr/bin/env python
# coding:utf-8

from flask import Flask,redirect,session
import functools

# 切换到每个页面时进行session检查
def require(func):
    @functools.wraps(func)
    def check_session(*args,**kwargs):
        if not session.get('name',None):
            return redirect('/login')
        return func(*args,**kwargs)
    return check_session