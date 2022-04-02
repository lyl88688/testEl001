#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
from logging import handlers

bugLevel = logging.DEBUG
filename="./log/runninglog.log"
#输出格式
fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
#备份文件数量
backCount = 3
#文件大小5M
maxTxtSpace = 5*1024*1024


#文件
logger = logging.getLogger(filename)
#日志级别
logger.setLevel(bugLevel)
#日志格式
formater = logging.Formatter(fmt)

#定义一个RotatingFileHandler，最大备份backupCount个文件，每个文件大小maxBytes,记入txt文件中
rHandler = handlers.RotatingFileHandler(filename, maxBytes=maxTxtSpace, backupCount=backCount)
rHandler.setLevel(bugLevel)
rHandler.setFormatter(formater)

#输出控制台
console = logging.StreamHandler()
console.setLevel(bugLevel)
console.setFormatter(formater)

logger.addHandler(rHandler)
#默认不在pycharm上打印，以日志形式记录。
# logger.addHandler(console)



#调试打印如下
# logger.info("User %s is loging" % '1')





