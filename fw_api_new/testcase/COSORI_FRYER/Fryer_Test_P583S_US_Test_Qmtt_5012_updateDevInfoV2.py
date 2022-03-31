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
import threading


#全局变量

exceptMethod = "updateDevInfoV2"
exceptRegion = deviceRegion
exceptPid = pid
exceptCid = device_cid
exceptAccountId = device_accountID
exceptPluginNameMcu = pluginNameMcu
exceptNewVersionMcu = newVersionMcu
exceptNewVersionUrlMcu = newVersionUrlMcu

exceptPluginNameMainFw = pluginNameMainFw
exceptNewVersionMainFw = newVersionMainFw
exceptNewVersionUrlMainFw = newVersionUrlMainFw

threads = []
#需要匹配的串口字符串变量，来源Qmtt协议。
comDataStr = '{"context":{"traceId":"[0-9]*","method":"updateDevInfoV2".*?"isMainFw":.*?}]}}'
#取决于串口获取到报文的时间
comTime = 800

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

        except Exception as e:
            print("=====异常=====", e)

    def comData(self):
        print("获取串口数据。。。。。")
        time.sleep(30)
        global  testComData
        testComData = qmttData().qmttInteraction(comTime=comTime, comDataStr=comDataStr)


    def testUpDevInfoqmtt(self):
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
            if testComData["data"]["wifiName"] and testComData["data"]["mac"] and testComData["data"]["routerMac"] and testComData["data"]["rssi"] \
                and testComData["data"]["BTMac"] :
                self.assertEqual(testComData["context"]["method"], exceptMethod)
                self.assertEqual(testComData["context"]["pid"], exceptPid)
                self.assertEqual(testComData["context"]["cid"], exceptCid)
                self.assertEqual(testComData["context"]["deviceRegion"], exceptRegion)

                self.assertEqual(testComData["data"]["initState"], "Upgrade")
                self.assertEqual(testComData["data"]["firmwareInfos"][0]["pluginName"], exceptPluginNameMcu)
                self.assertEqual(testComData["data"]["firmwareInfos"][0]["version"], exceptNewVersionMcu)
                self.assertEqual(testComData["data"]["firmwareInfos"][0]["isMainFw"], False)
                self.assertEqual(testComData["data"]["firmwareInfos"][0]["priority"], 0)
                self.assertEqual(testComData["data"]["firmwareInfos"][1]["pluginName"], pluginNameMainFw)
                self.assertEqual(testComData["data"]["firmwareInfos"][1]["version"], newVersionMainFw)
                self.assertEqual(testComData["data"]["firmwareInfos"][1]["isMainFw"], True)
                self.assertEqual(testComData["data"]["firmwareInfos"][1]["priority"], 1)

        except Exception as e:
            self.assertEqual(0, e)

if __name__ == "__main__":

    unittest.main(verbosity=1)


