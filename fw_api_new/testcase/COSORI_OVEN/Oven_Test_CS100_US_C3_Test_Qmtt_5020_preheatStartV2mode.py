# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、
#描述：
#==================================================


import unittest,json, ddt, threading,time
from lib.commonApi import *
from lib.serialComData import *
from unittestreport import rerun


#全局变量
"""
{'context': {'traceId': '1624937394902', 'method': 'cookStartV2', 'pid': 'v8w4b6hyvzj74ki1', 'cid': 'vssk1322d4864f0f800134db9b2080b5', 'deviceRegion': 'US'},
'data': {'accountId': '1516480', 'recipeId': 4, 'recipeType': 3, 'cookStartTime': 1624937394, 'workTime': 1800, 'workTemp': 180, 'mode': 'Bake', 'level': 4, 'workTempUnit': 'f', 'hasPreheat': 0}}
"""
modeCookMode = "Warm"
exceptMode = "Warm"  #测试模式
exceptRecipeId = 4  #对应菜单
exceptRecipeType = 3  #对应菜单类型
exceptMethod = "preheatEndV2"
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
cookStartVal = [["AirFry", 6, 150,1800],
                ["Bake", 4, 150, 1800],
                ["Broil", 7, 150, 1800],
                ["Defrost", 15, 150, 1800],
                ["Pizza", 3, 150, 1800],
                ["Roast", 5, 150, 1800],
                ["SlowCook", 14, 150,1800]]

#不支持预热
cookStartValTaost = ["Toast", 1, 480, 275, 5]


#需要匹配的串口字符串变量，来源Qmtt协议。
comDataStr = '{"context":{"traceId":"[0-9]*","method":"preheatEndV2".*?"preheatTempUnit":.*?}}'

#取决于串口获取到报文的时间
comTime = 240

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

    def methodQmtt(self, mode=modeCookMode, recipeId=exceptRecipeId, cookTemp=exceptTestFahval, cookTime=exceptTestTime, cookLevel=4 ,unit=exceptFahUnit):
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
            print(tsmode, tsrecipeId, tscookTemp, tscookTime)
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=tsmode, recipeId=tsrecipeId, cookTemp=tscookTemp, cookTime=tscookTime, preheatTemp=tspreheatTemp,unit=unit, cookLevel=cookLevel)
            time.sleep(60)

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=tsmode, recipeId=tsrecipeId, cookTemp=tscookTemp, cookTime=tscookTime, preheatTemp=tspreheatTemp,unit=unit, cookLevel=cookLevel)

    @ddt.data(*cookStartVal)
    #@ddt.unpac
    @rerun(count=3, interval=3)
    def testqmttMode(self, testval):
        print(time.strftime("%Y-%m-%d %X"))
        threads = []
        global tsmode, tsrecipeId, tscookTemp, tscookTime, tspreheatTemp
        tsmode = testval[0]
        tsrecipeId = testval[1]
        tscookTemp = testval[2]
        tscookTime = testval[3]
        tspreheatTemp = testval[2]
        t1 = threading.Thread(target=cosoriTest().comData)
        threads.append(t1)
        t2 = threading.Thread(target=cosoriTest().methodQmtt)
        threads.append(t2)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        try:
            print("\n匹配数据：", testComData)
            if testComData["context"]["traceId"]:
                self.assertEqual(testComData["context"]["method"], exceptMethod)
                self.assertEqual(testComData["context"]["pid"], exceptPid)
                self.assertEqual(testComData["context"]["cid"], exceptCid)
                self.assertEqual(testComData["context"]["deviceRegion"], exceptRegion)

                self.assertEqual(testComData["data"]["accountId"], exceptAccountId)
                self.assertEqual(testComData["data"]["preheatTemp"], testval[2])
                self.assertEqual(testComData["data"]["preheatTempUnit"], exceptFahUnit)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


