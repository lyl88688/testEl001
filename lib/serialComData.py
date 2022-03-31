#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'eleven'

import os,sys
sys.path.append(os.path.dirname(__file__))
import serial, re
import json
from lib.loggingTest import *
from lib import globalName

#全局变量
header = {"Content-Type":"application/json"}
#毫秒级时间戳
traceId = str(int(round(time.time() * 1000)))

class qmttData():
    """
    QMTT交互：设备主动上报数据给云端。
    :return:
    """
    def openSerial(self):
        ser = serial.Serial(port=globalName.portx, baudrate=globalName.brate, timeout=globalName.timex)  # 创建串口对象

        return ser

    def closeSerial(self):

        qmttData().openSerial().close()  # 关闭端口

    def qmttInteraction(self, comTime=300, comDataStr=""):
        print("========qmttInteraction========")
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
            Logger().getLog().debug("data=%s & i=%s" % (rownew, i))
            rownew1 += rownew

        # 匹配字符串数据
        fn = re.findall(comDataStr, rownew1)[0]
        # 将已编码的JSON字符串解码为Python对象
        testData = json.loads(fn)
        ser.close()
        Logger().getLog().info(testData)

        return testData


