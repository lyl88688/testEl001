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


modeCookMode = "Warm"
exceptMode = "Warm"  #测试模式
exceptRecipeId = 4  #对应菜单
exceptRecipeType = 3  #对应菜单类型
exceptMethod = "cookPauseV2"
exceptRegion = deviceRegion
exceptPid = pid
exceptCid = device_cid
exceptAccountId = device_accountID
exceptCodeResult = 0  # 预期结果
exceptTestFahval = 200
exceptTestDegval = 66
exceptTestTime = 1800
exceptlLevel = 4
exceptFahUnit = "f"
exceptDegUnit = "c"
exceptHasPreheat = 0
threads = []
#需要匹配的串口字符串变量，来源Qmtt协议。
comDataStr = '{"context":{"traceId":"[0-9]*","method":"cookPauseV2".*?"cookLastTime":.*?}}'

#取决于串口获取到报文的时间
comTime = 300

#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        commonFunc().debugLevel(method="setLogLevel",debugMode="DEBUG")
        commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        print("环境恢复。。。。")
        commonFunc().debugLevel(method="setLogLevel", debugMode="OFF")

    def cookstartQmtt(self, mode=exceptMode, recipeId=exceptRecipeId, cookTemp=exceptTestFahval, cookTime=exceptTestTime, unit=exceptFahUnit):
        """
        {'context': {'traceId': '1624937394902', 'method': 'cookStartV2', 'pid': 'v8w4b6hyvzj74ki1', 'cid': 'vssk1322d4864f0f800134db9b2080b5', 'deviceRegion': 'US'},
        'data': {'accountId': '1516480', 'recipeId': 4, 'recipeType': 3, 'cookStartTime': 1624937394, 'workTime': 1800, 'workTemp': 180, 'mode': 'Bake', 'level': 4, 'workTempUnit': 'f', 'hasPreheat': 0}}
        """
        print("=================开始测试模式下发=====================")
        try:
            print("======changeUnit=========")
            degUnit = commonFunc().commMethodApi(method="setTempUnit", unit=unit)
            time.sleep(5)

            print("======resCook=========")
            #method, mode="", recipeId="", cookTemp=180, cookTime=1800, unit="f",cookLevel=4, preheatTemp=0, readyStart=False)
            print(cookTemp, cookTime, unit)
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=mode, recipeId=recipeId, cookTemp=cookTemp, cookTime=cookTime, unit=unit)
            time.sleep(15)

            print("======pauseWorkRes=========")
            pauseWorkRes = commonFunc().commMethodApi(method="pauseWork")
            time.sleep(60)

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=mode, recipeId=recipeId, cookTemp=cookTemp, cookTime=cookTime, unit=unit)

    def comData(self):
        print("获取串口数据。。。。。")
        global  testComData
        testComData = qmttData().qmttInteraction(comTime=comTime, comDataStr=comDataStr)


    def testqmttfah(self):
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
            print(testComData)
            if testComData["data"]["cookLastTime"] and testComData["data"]["pauseStartTime"]:
                self.assertEqual(testComData["context"]["method"], exceptMethod)
                self.assertEqual(testComData["context"]["pid"], exceptPid)
                self.assertEqual(testComData["context"]["cid"], exceptCid)
                self.assertEqual(testComData["context"]["deviceRegion"], exceptRegion)
                self.assertEqual(testComData["data"]["accountId"], exceptAccountId)
                self.assertEqual(testComData["data"]["mode"], exceptMode)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


