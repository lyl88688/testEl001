# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、升级到测试版本，预期升级成功。（验证最新3个旧版本升级）

#描述：
#==================================================


import unittest
from lib.commonData import *
import json,ddt


#全局变量
pluginNameMcu = pluginNameMcu
newVersionMcu = newVersionMcu
newVersionUrlMcu = newVersionUrlMcu

#异常升级包分别：countrycode/wrong hwver/wrong md5/wrong model/wrong swver
updateOldMcuInfo = [["1.0.05", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/mcu/Countrycode/CAF-P583S-KUS_MCU_C1_ota_v1.0.05.bin"],
                    ["1.0.05", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/mcu/Wrong_HwVer/CAF-P583S-KUS_MCU_C1_ota_v1.0.05.bin"],
                    ["1.0.05", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/mcu/Wrong_MD5/CAF-P583S-KUS_MCU_C1_ota_v1.0.06_MD5.bin"],
                    ["1.0.05", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/mcu/Wrong_Model/CAF-P583S-KUS_MCU_C1_ota_v1.0.05.bin"],
                    ["1.0.05", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/mcu/Wrong_SwVer/CAF-P583S-KUS_MCU_C1_ota_v1.0.05.bin"]]


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
            cls.getVersionRes = commonFunc().getVersionInfo(typeVer=pluginNameMcu, versionVal=newVersionMcu)
            i = 0#避免网络原因导致无法升级成功，进入死循环。
            while json.loads(cls.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"] != newVersionMcu  and i < 3:
                    nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu,
                                                             versionName=newVersionMcu, versionUrl=newVersionUrlMcu)

                    time.sleep(240)
                    cls.getVersionRes = commonFunc().getVersionInfo(typeVer=pluginNameMcu, versionVal=newVersionMcu)
                    i += 1

        except Exception as e:
            print(e)



    @ddt.data(*updateOldMcuInfo)
    # @ddt.unpac
    def testMcuUpateVer(self, versionInfo):
        print("===================开始测试==========================")
        print(versionInfo[0], versionInfo[1])#0-版本号；1-版本路劲
        try:
            print("MCU升级到错误升级包的版本%s，并等待升级时间，固件升级中。。。。。。"%versionInfo[0])
            oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu, versionName=versionInfo[0], versionUrl=versionInfo[1])
            # print("获取当前版本信息")

            if json.loads(oldVerUpRes.text)["result"]["code"] == 0:
                time.sleep(240)
                self.getVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = newVersionMcu)
                self.assertEqual(json.loads(self.getVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], newVersionMcu)
            else:
                oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMcu,
                                                         versionName=versionInfo[0], versionUrl=versionInfo[1])
                time.sleep(240)
                self.getVerInfo = commonFunc().getVersionInfo(typeVer=pluginNameMcu, versionVal=newVersionMcu)

                self.assertEqual(json.loads(self.getVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], newVersionMcu)

        except Exception as e:
            self.getVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMcu, versionVal = newVersionMcu)
            self.assertEqual(json.loads(self.getVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"], e)

if __name__ == "__main__":
    unittest.main(verbosity=1)
