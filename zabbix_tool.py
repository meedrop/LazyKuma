#!/usr/bin/env python
# coding:utf-8

import json
import requests
import time
import traceback
from conf import config
from tools import logstdout

logs = logstdout.WriteLog('zabbix')

class zabbix():
    def __init__(self):
        self.url = config.zabbix_url
        self.user = config.zabbix_user
        self.passwd = config.zabbix_password
        self.headers = {"Content-Type": "application/json-rpc"}

    # 获取token
    def get_token(self):
        # headers = {"Content-Type": "application/json-rpc"}
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.passwd
            },
            "id": 1,
            "auth": None
        }
        try:
            r = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            logs.info("获取token: %s" % (r.json()))
            return r.json()['result']
        except:
            logs.error("Error: %s" % (traceback.format_exc()))

    # 获取主机参数
    def host_get(self,hosts):
        token = self.get_token()  # 传入主机名
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        hosts,
                    ]
                }
            },
            "auth": token,
            "id": 1
        }
        try:
            r = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            logs.info("获取主机参数: %s" % (r.json()))
            return r.json()["result"]
        except:
            logs.error("Error: %s" % (traceback.format_exc()))

    # 获取主机item信息
    def item_get(self,hostids,key):
        token = self.get_token()
        # hostids = self.host_get(hosts)["result"][0]["hostid"] # 传入主机名
        key_ = key # 传入itemkey名称
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": hostids,
                "search": {
                    "key_": key
                },
                "sortfield": "name"
            },
            "auth": token,
            "id": 1
        }
        try:
            r = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            logs.info("获取主机item信息: %s" % (r.json()))
            return r.json()["result"]
        except:
            logs.error("Error: %s" % (traceback.format_exc()))

    def history_get(self,itemid,time_from,time_till):
        token = self.get_token()
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": itemid,
                "sortfield": "clock", # 基于时间做排序输出list
                "sortorder": "ASC",   # 使用升序 用于图形展示
                "time_from": time_from,
                "time_till" : time_till,
                "limit": 60
            },
            "auth": token,
            "id": 1
        }
        try:
            r = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            logs.info("获取item历史数据: %s" % (r.json()))
            return r.json()["result"]
        except:
            logs.error("Error: %s" % (traceback.format_exc()))

# 获取hostid
# hostids = zabbix().host_get("Zabbix server")["result"][0]["hostid"]
# itemid = zabbix().item_get(hostids,"system.cpu.util[,idle]")["result"][0]["itemid"]
# zabbix().history_get(itemid,onehour_before,now)
# zabbix().item_get("Zabbix server","system.cpu.util[,idle]")

