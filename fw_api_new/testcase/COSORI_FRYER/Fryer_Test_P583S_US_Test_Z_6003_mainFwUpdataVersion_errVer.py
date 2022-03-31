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
pluginNameMainFw = pluginNameMainFw
newVersionMainFw = newVersionMainFw
newVersionUrlMainFw = newVersionUrlMainFw

updateOldMainFwInfo = [["1.0.04", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/wifi/Countrycode/CAF-P583S-KUS_WIFI_C1_ota_Countrycode_v1.0.04.rel.bin"],
                       ["1.0.04", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/wifi/Wrong_HwVer/CAF-P583S-KUS_WIFI_C1_ota_v1.0.04.rel2.bin"],
                       ["1.0.04", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/wifi/Wrong_MD5/CAF-P583S-KUS_WIFI_C1_ota_v1.0.04.rel.bin"],
                       ["1.0.04", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/wifi/Wrong_Model/CAF-P583S-KUS_WIFI_C1_ota_v1.0.04.rel3.bin"],
                       ["1.0.04", "http://192.168.23.96:8888/firmware-debug/eleventest/p583/wifi/Wrong_SwVer/CAF-P583S-KUS_WIFI_C1_ota_v1.0.04.rel.bin"]]


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
            cls.getVersionRes = commonFunc().getVersionInfo(typeVer=pluginNameMainFw, versionVal=newVersionMainFw)
            i = 0#避免网络原因导致无法升级成功，进入死循环。
            while json.loads(cls.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"] != newVersionMainFw  and i < 3:
                    nweVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=newVersionMainFw,
                                                             versionName=newVersionMainFw, versionUrl=newVersionUrlMainFw)

                    time.sleep(240)
                    cls.getVersionRes = commonFunc().getVersionInfo(typeVer=pluginNameMainFw, versionVal=newVersionMainFw)
                    i += 1

        except Exception as e:
            print(e)



    @ddt.data(*updateOldMainFwInfo)
    # @ddt.unpac
    def testMcuUpateVer(self, versionInfo):
        print("===================开始测试==========================")
        print(versionInfo[0], versionInfo[1])#0-版本号；1-版本路劲
        try:
            print("MCU升级到错误升级包的版本%s，并等待升级时间，固件升级中。。。。。。"%versionInfo[0])
            oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=versionInfo[0], versionUrl=versionInfo[1])
            # print("获取当前版本信息")

            if json.loads(oldVerUpRes.text)["result"]["code"] == 0:
                time.sleep(240)

                self.getVerInfo = commonFunc().getVersionInfo(typeVer=pluginNameMainFw, versionVal=newVersionMainFw)
                self.assertEqual(json.loads(self.getVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], newVersionMainFw)

            else:
                oldVerUpRes = commonFunc().commMethodApi(method="upFirmware", pluginName=pluginNameMainFw, versionName=versionInfo[0], versionUrl=versionInfo[1])

                time.sleep(240)
                self.getVerInfo = commonFunc().getVersionInfo(typeVer=pluginNameMainFw, versionVal=newVersionMainFw)

                self.assertEqual(json.loads(self.getVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], newVersionMainFw)

        except Exception as e:
            self.getVerInfo = commonFunc().getVersionInfo(typeVer = pluginNameMainFw, versionVal = newVersionMainFw)
            self.assertEqual(json.loads(self.getOldVerInfo.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"], e)

if __name__ == "__main__":
    unittest.main(verbosity=1)
