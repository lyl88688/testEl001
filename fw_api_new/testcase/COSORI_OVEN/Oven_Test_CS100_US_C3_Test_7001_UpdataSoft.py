# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、升级到测试版本，预期升级成功。（验证最新3个旧版本升级）

#描述：
#==================================================


import unittest, requests,time
from lib.commonData import *
import json,ddt


#全局变量
pluginNameMcu = pluginNameMcu
newVersionMcu = newVersionMcu
newVersionUrlMcu = newVersionUrlMcu
pluginNameMainFw = pluginNameMainFw
newVersionMainFw = newVersionMainFw
newVersionUrlMainFw = newVersionUrlMainFw

#验证最新3个旧版本升级
# updateOldMcuInfo = [["3.0.03", "http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mcuFw-C3/v3.0.03/CS100_MCU_C3_US_ota_v3.0.03.bin"],
#               ["3.0.03", "http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mcuFw-C3/v3.0.03/CS100_MCU_C3_US_ota_v3.0.03.bin"]]

# updateOldMcuInfo = [["3.0.03", "http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mcuFw-C3/v3.0.03/CS100_MCU_C3_US_ota_v3.0.03.bin"]]

#验证最新3个旧版本升级
# updateOldMainFwInfo = [["1.1.02", "http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mainFirmware/v1.1.02/CS100-AO_US_ota_v1.1.02.rel.bin"],
#               ["1.2.00", "http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mainFirmware/v1.2.00/CS100-AO_US_ota_v1.2.00.rel.bin"]]

# updateOldMainFwInfo = [["1.2.00", "http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mainFirmware/v1.2.00/CS100-AO_US_ota_v1.2.00.rel.bin"]]


i = 0
updateOldMainFwInfo = []
updateOldMcuInfo = []
while i < int(updateTime):
    i += 1
    updateOldMcu = []
    updateOldMainFw = []
    if i <= int(updateTime):
        updateOldMcu.append(oldVersionMcu)
        updateOldMcu.append(oldVersionUrlMcu)
        updateOldMainFw.append(oldVersionMainFw)
        updateOldMainFw.append(oldVersionUrlMainFw)

    updateOldMcuInfo.append(updateOldMcu)
    updateOldMainFwInfo.append(updateOldMainFw)

print(updateOldMcuInfo,updateOldMainFwInfo)

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        commonFunc().commMethodApi(method="endCook")

    @classmethod
    def tearDownClass(cls):
        """
        环境恢复：判断mcu和mainFw是否最新，是--pass，否--再进行判断：mcu正确--升级mainFw，mainFw正确，升级mcu。
        :return:
        """
        try:
            cls.getOldVerInfo = commonFunc().getVersionInfo(typeVer=pluginNameMcu, versionVal=newVersionMcu)
            i = 0#避免网络原因导致无法升级成功，进入死循环。
            while json.loads(cls.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"] != newVersionMcu or json.loads(cls.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"] != newVersionMainFw and i < 5:
                if json.loads(cls.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"] == newVersionMcu:
                    nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=newVersionMainFw, versionUrl=newVersionUrlMainFw)
                    cls.getOldVerInfo = commonFunc().getVersionInfo(typeVer=pluginNameMcu, versionVal=newVersionMcu)
                    i += 1
                else:
                    nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu, versionName=newVersionMcu, versionUrl=newVersionUrlMcu)
                    cls.getOldVerInfo = commonFunc().getVersionInfo(typeVer=pluginNameMcu, versionVal=newVersionMainFw)
                    i += 1

        except Exception as e:
            print(e)

    @ddt.data(*updateOldMcuInfo)
    # @ddt.unpac
    def testMcuUpateVer(self, versionInfo):
        print("===================开始测试==========================")
        print(versionInfo[0], versionInfo[1])#0-版本号；1-版本路劲
        try:
            print("MCU升级到上一个验证升级版本%s，并等待升级时间，固件升级中。。。。。。"%versionInfo[0])
            oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu, versionName=versionInfo[0], versionUrl=versionInfo[1])
            # print("获取当前版本信息")
            self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = versionInfo[0])

            if json.loads(oldVerUpRes.text)["result"]["code"] == 0:
                i = 0
                while json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"] != versionInfo[0] and i <= 1:
                    print("获取旧版本版本号次数%d"%i)
                    oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu, versionName=versionInfo[0],
                                                             versionUrl=versionInfo[1])

                    self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = versionInfo[0])
                    i += 1

                self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], versionInfo[0])

                if json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"] == versionInfo[0]:
                    print("MCU升级最新版本---->%s，并等待升级完成时间，固件升级中。。。。。。" % newVersionMcu)
                    nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu, versionName=newVersionMcu, versionUrl=newVersionUrlMcu)

                    self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = newVersionMcu)
                    i = 0
                    while json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"] != newVersionMcu and i <= 1:
                        print("获取新版本版本号次数%d" % i)
                        nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu, versionName=newVersionMcu,
                                                                 versionUrl=newVersionUrlMcu)

                        self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = newVersionMcu)
                        i += 1

                else:
                    pass
            else:
                self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], versionInfo[0])

            self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], newVersionMcu)

        except Exception as e:
            self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = newVersionMcu)
            self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], e)

    @ddt.data(*updateOldMainFwInfo)
    #@ddt.unpac
    def testMainFwUpateVer(self, versionMainFwInfo):
        print("===================开始测试==========================")
        print(versionMainFwInfo[0], versionMainFwInfo[1])#0-版本号；1-版本路劲
        try:
            print("WIFI升级到上一个验证升级版本%s，并等待升级时间，固件升级中。。。。。。"%versionMainFwInfo[0])
            oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=versionMainFwInfo[0], versionUrl=versionMainFwInfo[1])

            self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMainFw, versionVal = versionMainFwInfo[0])
            if json.loads(oldVerUpRes.text)["result"]["code"] == 0:
                i = 0
                while json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"] != versionMainFwInfo[0] and i <= 1:
                    print("获取旧版本版本号次数%d"%i)
                    oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=versionMainFwInfo[0],
                                                             versionUrl=versionMainFwInfo[1])
                    self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMainFw, versionVal = versionMainFwInfo[0])
                    i += 1

                self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], versionMainFwInfo[0])

                if json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"] == versionMainFwInfo[0]:
                    print("WIFI升级最新版本---->%s，并等待升级完成时间，固件升级中。。。。。。" % newVersionMainFw)
                    nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=newVersionMainFw, versionUrl=newVersionUrlMainFw)

                    self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMainFw, versionVal = newVersionMainFw)
                    i = 0
                    while json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"] != newVersionMainFw and i <= 1:
                        print(json.loads(self.getOldVerInfo.text))
                        print("获取新版本版本号次数%d" % i)
                        nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=newVersionMainFw,
                                                                 versionUrl=newVersionUrlMainFw)

                        self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMainFw, versionVal = newVersionMainFw)
                        i += 1
                else:
                    pass
            else:
                self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], versionMainFwInfo[0])

            self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], newVersionMainFw)

        except Exception as e:
            self.getOldVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMainFw, versionVal = newVersionMainFw)
            self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], e)

if __name__ == "__main__":
    unittest.main(verbosity=1)
