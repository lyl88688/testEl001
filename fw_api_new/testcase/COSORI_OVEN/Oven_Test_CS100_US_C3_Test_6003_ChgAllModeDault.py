# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#修改预设菜单默认值，预期修改成功。
#描述：
#==================================================


import unittest, requests,time
from lib.commonData import *
import json,ddt,random


#全局变量
modeDaultVal = {"Toast":[480, 250,4],
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

modeDaultValChg = {"Toast":[480, 300, 5],
    "Bake":[3600, 300],
    "Broil":[1200, 400],
    "PreHeat":[300, 400],
    "Dehydrate":[10800, 100],
    "AirFry":[1200, 300],
    "Pizza":[900, 400],
    "Fermentation":[3000, 80],
    "SlowCook":[18000, 200],
    "Defrost":[3600, 200],
    "Roast":[1800, 350],
    "Warm":[3600, 200]
}

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        commonFunc().commMethodApi(method="endCook")
        time.sleep(2)
        for i in modeDaultValChg:
            print(i)
            time.sleep(2)
            if i == "Toast":
                #{"mode":mode,"cookTemp":cookTemp,"cookSetTime":cookTime,"tempUnit":unit, "level":cookLevel}
                commonFunc().commMethodApi(method="updatePresetRecipe", mode=i, cookTemp=modeDaultValChg[i][1],
                                                   cookTime=modeDaultValChg[i][0], cookLevel=modeDaultValChg[i][2])
            elif i == "PreHeat":
                pass
            else:
                commonFunc().commMethodApi(method="updatePresetRecipe", mode=i, cookTemp=modeDaultValChg[i][1],cookTime=modeDaultValChg[i][0])

    def tearDown(self):
        commonFunc().commMethodApi(method="resetAllPresetRecipe")

    def testChangeDaultVal(self):
        print("=================开始测试=====================")
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
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["level"], modeDaultValChg["Toast"][2])

                else:
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                                     modeDaultValChg[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                                     modeDaultValChg[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][1])

            else:
                #待补充摄氏度
                pass


if __name__ == "__main__":
    unittest.main(verbosity=1)
