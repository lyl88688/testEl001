# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、
#描述：
#==================================================


import unittest
from lib.commonData import *
import json, ddt, threading


#全局变量
"""
{'context': {'traceId': '1624937394902', 'method': 'cookStartV2', 'pid': 'v8w4b6hyvzj74ki1', 'cid': 'vssk1322d4864f0f800134db9b2080b5', 'deviceRegion': 'US'},
'data': {'accountId': '1516480', 'recipeId': 4, 'recipeType': 3, 'cookStartTime': 1624937394, 'workTime': 1800, 'workTemp': 180, 'mode': 'Bake', 'level': 4, 'workTempUnit': 'f', 'hasPreheat': 0}}
"""


modeCookMode = "Roast"
exceptMode = "Roast"  #测试模式
exceptRecipeId = 13  #对应菜单
exceptRecipeType = 3  #对应菜单类型
exceptMethod = "switchTemperatureUnitV2"
exceptRegion = deviceRegion
exceptPid = pid
exceptCid = device_cid
exceptAccountId = device_accountID
exceptConfigModel = device_configModule
exceptVersionMainFw = newVersionMainFw
exceptCodeResult = 0  # 预期结果
exceptTestFahval = 200
exceptTestDegval = 80
exceptTestTime = 1800
exceptlLevel = 4
exceptFahUnit = "f"
exceptDegUnit = "c"
exceptHasPreheat = 0
threads = []
#需要匹配的串口字符串变量，来源Qmtt协议。
comDataStr = '{"context":{"traceId":"[0-9]*","method":"switchTemperatureUnitV2".*?"changeReason":.*?}}'
#取决于串口获取到报文的时间
comTime = 150

#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        commonFunc().debugLevel(method="setLogLevel",debugMode="DEBUG")
        commonFunc().commMethodApiNew(method="endCook")
        degUnit = commonFunc().commMethodApi(method="setTempUnit", unit=exceptDegUnit)

    def tearDown(self):
        print("环境恢复。。。。")
        commonFunc().debugLevel(method="setLogLevel", debugMode="OFF")


    def cookstartQmtt(self, cookTemp=exceptTestFahval, cookTime=exceptTestTime, unit=exceptFahUnit):
        """
        {'context': {'traceId': '1624937394902', 'method': 'cookStartV2', 'pid': 'v8w4b6hyvzj74ki1', 'cid': 'vssk1322d4864f0f800134db9b2080b5', 'deviceRegion': 'US'},
        'data': {'accountId': '1516480', 'recipeId': 4, 'recipeType': 3, 'cookStartTime': 1624937394, 'workTime': 1800, 'workTemp': 180, 'mode': 'Bake', 'level': 4, 'workTempUnit': 'f', 'hasPreheat': 0}}
        """
        print("=================开始测试=====================")
        try:
            time.sleep(15)
            print("======changeUnit=========")
            degUnit = commonFunc().commMethodApi(method="setTempUnit", unit=exceptFahUnit)

        except Exception as e:
            print("=====异常=====", e)

    def comData(self):
        print("获取串口数据。。。。。")
        global  testComData
        time.sleep(8)
        testComData = qmttData().qmttInteraction(comTime=comTime, comDataStr=comDataStr)

    def testqmttfahunit(self):
        threads = []
        t1 = threading.Thread(target=cosoriTest().comData)
        threads.append(t1)
        t2 = threading.Thread(target=cosoriTest().cookstartQmtt)
        threads.append(t2)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        try:
            # print(testComData)
            if testComData["context"]["cause"]:
                self.assertEqual(testComData["context"]["method"], exceptMethod)
                # self.assertEqual(testComData["context"]["pid"], exceptPid)
                self.assertEqual(testComData["context"]["cid"], exceptCid)
                self.assertEqual(testComData["context"]["deviceRegion"], exceptRegion)

                self.assertEqual(testComData["data"]["tempUnit"], exceptFahUnit)
                self.assertEqual(testComData["context"]["configModel"], exceptConfigModel)
                self.assertEqual(testComData["context"]["mainFwVersion"], exceptVersionMainFw)

        except Exception as e:
            self.assertEqual(0, e)

if __name__ == "__main__":

    unittest.main(verbosity=1)


