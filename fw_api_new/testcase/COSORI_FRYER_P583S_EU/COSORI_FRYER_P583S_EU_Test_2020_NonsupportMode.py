# _*_ coding:utf-8 _*_

# ==================================================
#
#
#
# 步骤
# 1、
# 描述：测试mode
# ==================================================


import unittest, requests, time
from lib.commonData import *
from lib import loggingTest
import json, ddt, random

#格式recipeId(菜单ID)，mode
cookDalVal = 350 #根据下面范围设置
cookDalTime = 600 #根据下面范围设置

nonSupportMode = [
    [4, "Shrimp"],
    [11, "Eggtart"],
    [18, "Dehydrate"],
    [13, "PreHeat"],
    [14, "SlowCook"],
    [8, "Cookies"],
    [9, "Rotisserie"],
    [2, "Bagel"],
    [3, "Pizza"],
    [12, "Warm"],
]

# 测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        commonFunc().commMethodApiNew(method="endCook")
        print("======changeUnit=========")
        degUnit = commonFunc().commMethodApi(method="setTempUnit", unit="f")

    def tearDown(self):
        pass



    @ddt.data(*nonSupportMode)
    # @ddt.unpac
    def testNonsupportMode(self, modeVal):
        print("=================开始测试模式下发=====================", modeVal)
        try:
            print("======resCook=========")
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=modeVal[1], recipeId=modeVal[0], cookTemp=cookDalVal, cookTime=cookDalTime)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(resCook.text)["result"]["code"], 11000000 )#参数不合法

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)['result']["result"]['stepArray'][0]['mode'],e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

if __name__ == "__main__":
    unittest.main(verbosity=1)
