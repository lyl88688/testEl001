# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、设置模式
#2、华氏度测试
#3、摄氏度测试
#4、时间测试
#描述：
#==================================================


import unittest, requests,time
from lib.commonData import *
import json,ddt,random


#全局变量
modeDaultVal = {"Toast":[4],
    "Bake":[1800, 350],
    "Broil":[600, 450],
    "PreHeat":[300, 400],
    "Dehydrate":[21600, 150],
    "AirFry":[1500, 380],
    "Pizza":[720, 450],
    "Fermentation":[3600, 90],
    "SlowCook":[21600, 250],
    "Defrost":[1800, 150],
    "Roast":[3600, 400],
    "Warm":[1800, 180]
}

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        commonFunc().commMethodApi(method="endCook")

    def tearDown(self):
        pass

    def testGetModeDault(self):
        print("=================开始测试模式默认值=====================")
        try:
            self.getPreseRecipeDault = commonFunc().commMethodApi(method="getPresetRecipe")

        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"], e)

        for i in  range(len(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"])):
            print(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i], i)
            self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["tempUnit"], "f")
            if json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["tempUnit"] == "f":
                if json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Toast":
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["level"], modeDaultVal["Toast"][0])

                else:
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                                     modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                                     modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][1])

            else:
                #待补充摄氏度
                pass

if __name__ == "__main__":
    unittest.main(verbosity=1)
