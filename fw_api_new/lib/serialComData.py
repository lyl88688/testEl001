#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
串口及串口数据处理

"""

__author__ = 'eleven'

import os,sys,time
sys.path.append(os.path.dirname(__file__))
import serial, re
from requests.packages import urllib3
# 禁用安全请求警告
urllib3.disable_warnings()
sys.path.append(os.path.dirname(__file__))
import json
from lib.logGet import *
#全局变量
header = {"Content-Type":"application/json"}

#毫秒级时间戳
traceId = str(int(round(time.time() * 1000)))
from lib.globalName import *


class qmttData():
    """
    QMTT交互：设备主动上报数据给云端。
    :return:
    """
    def openSerial(self):
        try:
            self.ser = serial.Serial(port=portx, baudrate=brate, timeout=timex)  # 创建串口对象
        except:
            logger.error(" openSerial 打开串口失败。")

        return self.ser

    def closeSerial(self):
        try:
            qmttData().openSerial().close()  # 关闭端口
        except:
            logger.error(" closeSerial 关闭串口失败。")


    def qmttInteraction(self, comTime=300, comDataStr=""):
        logger.debug("========qmttInteraction========")
        """
        QMTT交互：
        :return:{'context': {'traceId': '1624937394902', 'method': 'cookStartV2', 'pid': 'v8w4b6hyvzj74ki1', 'cid': 'vssk1322d4864f0f800134db9b2080b5', 'deviceRegion': 'US'},
        'data': {'accountId': '1516480', 'recipeId': 4, 'recipeType': 3, 'cookStartTime': 1624937394, 'workTime': 1800, 'workTemp': 180, 'mode': 'Bake', 'level': 4, 'workTempUnit': 'f', 'hasPreheat': 0}}
        """
        rownew1 = ""
        ser = qmttData().openSerial()

        i = 0
        while i < comTime:
            data = ser.readline()
            # print(data, i)

            row = data.decode("utf-8")
            if row == "":
                continue
            rownew = row.replace('\r', '').replace('\n', '').replace('\t', '')
            i += 1
            rownew1 += rownew

        logger.debug("qmttInteraction 串口数据 = %s" % rownew1)
        # 匹配字符串数据
        fn = re.findall(comDataStr, rownew1)[0]
        # 将已编码的JSON字符串解码为Python对象
        testData = json.loads(fn)
        ser.close()
        logger.info(testData)

        return testData