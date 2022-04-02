#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
Api接口方法（method, url, data, json, **）

"""
from lib.logGet import *
import requests

class ResquestApi:
    def __init__(self):
        pass

    def resApi(self, method, headers, url, data, json, **kwargs):

        if method == "post":
            try:
                self.res = requests.post(url=url, headers=headers, json=json, **kwargs)
                return self.res
            except Exception as e:
                logger.error(" resApi post 出错: %s " % e)

        elif method == "get":
            try:
                self.res = requests.get(url=url, headers=headers, data=data, **kwargs)
                return self.res
            except Exception as e:
                logger.error(" resApi get 出错: %s " % e)

        elif method == "put":
            try:
                self.res = requests.put(url=url, headers=headers, json=json, **kwargs)
                return self.res
            except Exception as e:
                logger.error(" resApi put 出错: %s " % e)

        elif method == "delete":
            try:
                self.res = requests.delete(url=url, headers=headers, json=json, **kwargs)
                return self.res
            except Exception as e:
                logger.error(" resApi put 出错: %s " % e)
        else:
            try:
                self.res = requests.request(method, url=url, headers=headers, json=json, **kwargs)
                return self.res
            except Exception as e:
                logger.error(" resApi method 出错: %s " % e)










