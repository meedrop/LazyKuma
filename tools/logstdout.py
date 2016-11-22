#!/usr/bin/env python
# coding:utf-8

import logging
import logging.handlers
import datetime

def WriteLog(logName):
    date = datetime.datetime.now() .strftime('%Y-%m-%d')
    file = '/tmp/logs-%s' % (date)
    level = logging.DEBUG
    # 定义日志格式
    format = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)2d]-%(funcName)s %(levelname)s %(message)s')
    handler = logging.handlers.RotatingFileHandler(file,mode='a',maxBytes=100*1024*1024,backupCount=100)
    handler.setFormatter(format)
    # 实例化一个日志对象
    logger = logging.getLogger(logName)         # 设置实例名
    logger.addHandler(handler)                  # 设置实例属性
    logger.setLevel(level)                      # 设置实例日志级别
    return logger                               # 函数最终将实例化的logger对象返回，后面直接调用即可
