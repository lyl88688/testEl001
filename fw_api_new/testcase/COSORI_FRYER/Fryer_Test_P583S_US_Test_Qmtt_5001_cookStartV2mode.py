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
modeCookMode = "Bake"
exceptMode = "Bake"  #测试模式
exceptRecipeId = 9  #对应菜单
exceptRecipeType = 3  #对应菜单类型
exceptMethod = "cookStartV2"
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
#mode=mode, recipeId=recipeId, cookTemp=cookTemp, cookTime=cookTime
cookStartVal = [["AirFry", 14, 265,600],
                ["Bake", 9, 265, 600],
                ["Broil", 17, 355, 600],
                ["Reheat", 16, 300, 600],
                ["Chicken", 2, 360, 600],
                ["Frozen", 5, 360,600],
                ["Seafood", 3, 330, 600],
                ["Roast", 13, 175, 600],
                ["Veggies", 15, 320,600],
                ["French fries", 6, 350,600],
                ["Steak", 1, 350,600]]



#需要匹配的串口字符串变量，来源Qmtt协议。
comDataStr = '{"context":{"traceId":"[0-9]*","method":"cookStartV2".*?"changeReason":.*?}}'

#取决于串口获取到报文的时间
comTime = 260

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        commonFunc().debugLevel(method="setLogLevel",debugMode="DEBUG")
        commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        print("环境恢复。。。。")
        commonFunc().debugLevel(method="setLogLevel", debugMode="OFF")

    def comData(self):
        print("获取串口数据。。。。。")
        global  testComData
        testComData = qmttData().qmttInteraction(comTime=comTime, comDataStr=comDataStr)

    def cookstartQmtt(self, mode=modeCookMode, recipeId=exceptRecipeId, cookTemp=exceptTestFahval, cookTime=exceptTestTime, cookLevel=4 ,unit=exceptFahUnit):
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
            print(tsmode, tsrecipeId, tscookTemp, tscookTime)
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=tsmode, recipeId=tsrecipeId, cookTemp=tscookTemp, cookTime=tscookTime, unit=unit, cookLevel=cookLevel)
            time.sleep(30)

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=mode, recipeId=recipeId, cookTemp=cookTemp, cookTime=cookTime, unit=unit)

    @ddt.data(*cookStartVal)
    #@ddt.unpac
    def testqmttMode(self, testval):
        # global testval
        threads = []
        global tsmode, tsrecipeId, tscookTemp, tscookTime
        tsmode = testval[0]
        tsrecipeId = testval[1]
        tscookTemp = testval[2]
        tscookTime = testval[3]
        t1 = threading.Thread(target=cosoriTest().comData)
        threads.append(t1)
        t2 = threading.Thread(target=cosoriTest().cookstartQmtt)
        # t2 = threading.Thread(target=cosoriTest().cookstartQmtt(mode=testval[0], recipeId=testval[1], cookTemp=testval[2], cookTime=testval[3]))
        threads.append(t2)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        try:
            print(testComData)
            if testComData["data"]["cookStartTime"] and testComData["data"]["changeReason"]:
                self.assertEqual(testComData["context"]["method"], exceptMethod)
                self.assertEqual(testComData["context"]["pid"], exceptPid)
                self.assertEqual(testComData["context"]["cid"], exceptCid)
                self.assertEqual(testComData["context"]["deviceRegion"], exceptRegion)
                self.assertEqual(testComData["data"]["accountId"], exceptAccountId)
                self.assertEqual(testComData["data"]["recipeId"], testval[1])
                self.assertEqual(testComData["data"]["recipeType"], exceptRecipeType)
                self.assertEqual(testComData["data"]["workTime"], testval[3])
                self.assertEqual(testComData["data"]["workTemp"], testval[2])
                self.assertEqual(testComData["data"]["mode"], testval[0])
                # self.assertEqual(testComData["data"]["level"], exceptlLevel)
                self.assertEqual(testComData["data"]["workTempUnit"], exceptFahUnit)
                self.assertEqual(testComData["data"]["hasPreheat"], exceptHasPreheat)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


