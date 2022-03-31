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

modeCookMode = "Roast"
exceptMode = "Roast"  #测试模式
exceptRecipeId = 13  #对应菜单
exceptRecipeType = 3  #对应菜单类型
exceptMethod = "reportFirmUpV2"
exceptRegion = deviceRegion
exceptPid = pid
exceptCid = device_cid
exceptAccountId = device_accountID
pluginNameMainFw = pluginNameMainFw
newVersionMainFw = newVersionMainFw
newVersionUrlMainFw = newVersionUrlMainFw

threads = []
#需要匹配的串口字符串变量，来源Qmtt协议。
comDataStr = '{"context":{"traceId":"[0-9]*","method":"reportFirmUpV2".*?"percent":.*?}}}'
#取决于串口获取到报文的时间
comTime = 400

comDataStr_10 = '{"context":{"traceId":"[0-9]*","method":"reportFirmUpV2".*?"percent":10}}}'
comDataStr_20 = '{"context":{"traceId":"[0-9]*","method":"reportFirmUpV2".*?"percent":20}}}'
comDataStr_30 = '{"context":{"traceId":"[0-9]*","method":"reportFirmUpV2".*?"percent":30}}}'


#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        commonFunc().debugLevel(method="setLogLevel",debugMode="DEBUG")
        commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        print("环境恢复。。。。")
        commonFunc().debugLevel(method="setLogLevel", debugMode="OFF")
        time.sleep(30)

    def mainFwUpateVer(self):
        print("=================开始测试=====================")
        try:
            time.sleep(5)
            versionUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=newVersionMainFw,
                                                     versionUrl=newVersionUrlMainFw)
            time.sleep(30)

        except Exception as e:
            print("=====异常=====", e)

    def comData(self):
        print("获取串口数据。。。。。")
        global  testComData
        testComData = qmttData().qmttInteraction(comTime=comTime, comDataStr=comDataStr)


    def testUpWifiqmtt(self):
        threads = []
        t1 = threading.Thread(target=cosoriTest().comData)
        threads.append(t1)
        t2 = threading.Thread(target=cosoriTest().mainFwUpateVer)
        threads.append(t2)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        try:
            print(testComData)
            if testComData["data"]["upgradeStatus"]["status"] and testComData["data"]["upgradeStatus"]["percent"]:
                self.assertEqual(testComData["context"]["method"], exceptMethod)
                self.assertEqual(testComData["context"]["pid"], exceptPid)
                self.assertEqual(testComData["context"]["cid"], exceptCid)
                self.assertEqual(testComData["context"]["deviceRegion"], exceptRegion)

                self.assertEqual(testComData["data"]["upgradeStatus"]["pluginName"], pluginNameMainFw)
                self.assertEqual(testComData["data"]["upgradeStatus"]["currentVersion"], newVersionMainFw)
                self.assertEqual(testComData["data"]["upgradeStatus"]["latestVersion"], newVersionMainFw)
                self.assertEqual(testComData["data"]["upgradeStatus"]["fwUrl"], newVersionUrlMainFw)
                self.assertEqual(testComData["data"]["upgradeStatus"]["isMainFw"], True)
                self.assertEqual(testComData["data"]["upgradeStatus"]["priority"], 1)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


