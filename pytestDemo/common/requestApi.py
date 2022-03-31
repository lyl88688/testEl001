#!/usr/bin/python
# -*- coding: UTF-8 _*_

"""
封装request

"""

import requests
import logging


class RequestsApi:
    def getReq(self, url, params, **kw):
        # '''封装一个get方法，发送get请求'''
        try:
            res = requests.get(url, json=params, **kw)
        except :
            logging.error(" getReq 请求响应失败")
        else:
            return res

    def postReq(self, url, data, **kw):
        try:
            res = requests.post(url, json=data, **kw)
        except:
            logging.error(" postReq 请求响应失败")
        else:
            return res

    def methodReq(self, method, url, data=None, **kw):
        """
        封装关于request中post\get\delete等方法

        """
        if method.lower == 'get':
            return self.getReq(url, json=data, **kw)
        elif method.lower == 'post':
            return self.postReq(url, json=data, **kw)
        else:
            return requests.request(method, url, **kw)