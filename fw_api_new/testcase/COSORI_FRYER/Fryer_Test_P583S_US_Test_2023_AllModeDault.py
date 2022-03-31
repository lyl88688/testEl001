# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、查看默认值。
#2、修改预设菜单默认值，预期修改成功。
#描述：
#==================================================


import unittest
from lib.commonData import *
import json,ddt


#全局变量
modeDaultVal = {"Steak":[480, 400, 205],
    "Chicken":[1200, 390, 200],
    "Seafood":[480, 375, 190],
    "Frozen":[720, 395, 200],
    "French fries":[1200, 385, 195],
    "AirFry":[600, 360, 180],
    "Veggies":[360, 385, 195],
    "Bake":[1200, 320, 160],
    "Roast":[600, 400, 205],
    "Reheat":[300, 350, 175],
    "Keep Warm":[1800, 175, 80],
    "Broil":[600, 400,205],
}

modeDaultValChg = {"Steak":[420, 380, 200],
    "Chicken":[1260, 380, 190],
    "Seafood":[420, 380, 195],
    "Frozen":[660, 355, 175],
    "French fries":[1560,390, 200],
    "AirFry":[1260, 390, 200],
    "Veggies":[540, 350, 170],
    "Bake":[1260, 345, 190],
    "Roast":[1160, 395, 190],
    "Reheat":[660, 390, 200],
    "Keep Warm":[1860, 190, 95],
    "Broil":[660, 390,200],
}

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        commonFunc().commMethodApi(method="resetAllPresetRecipe")

    def testChangeDaultHafVal(self):
        print("=================开始测试=====================")

        try:
            degUnit = commonFunc().commMethodApi(method="setTempUnit", unit="f")

            time.sleep(2)
            print("=================开始测试默认值=====================")
            self.getPreseRecipeDault = commonFunc().commMethodApi(method="getPresetRecipe")
            for i in range(len(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"])):
                print(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i])
                self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                                 modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                                 modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][1])

            print("=================开始测试修改默认值=====================")
            for i in modeDaultValChg:
                print(i)
                time.sleep(2)
                if i == "Toast":
                    commonFunc().commMethodApi(method="updatePresetRecipe", mode=i, cookTemp=modeDaultValChg[i][1],
                                               cookTime=modeDaultValChg[i][0], cookLevel=modeDaultValChg[i][2])
                elif i == "PreHeat":
                    pass
                else:
                    commonFunc().commMethodApi(method="updatePresetRecipe", mode=i, unit="f",cookTemp=modeDaultValChg[i][1],
                                               cookTime=modeDaultValChg[i][0])

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
                # elif json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "AirFry" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Reheat" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Roast" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Bake" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Broil":
                #
                #     self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                #         modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                #
                #     self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                #         modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][1])

                else:
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                                     modeDaultValChg[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                                     modeDaultValChg[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][1])

            else:
                self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["tempUnit"], "f")


    def testChangeDaultDegVal(self):
        print("=================开始测试=====================")

        try:
            degUnit = commonFunc().commMethodApi(method="setTempUnit", unit="c")
            time.sleep(2)
            print("=================开始测试默认值=====================")
            self.getPreseRecipeDault = commonFunc().commMethodApi(method="getPresetRecipe")
            for i in range(len(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"])):
                print(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i])
                self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                                 modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                                 modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][2])

            print("=================开始测试修改默认值=====================")
            for i in modeDaultValChg:
                print(i)
                time.sleep(2)
                if i == "Toast":
                    commonFunc().commMethodApi(method="updatePresetRecipe", mode=i, unit="c",cookTemp=modeDaultValChg[i][1],
                                               cookTime=modeDaultValChg[i][0], cookLevel=modeDaultValChg[i][2])
                elif i == "PreHeat":
                    pass
                else:
                    commonFunc().commMethodApi(method="updatePresetRecipe", mode=i, unit="c", cookTemp=modeDaultValChg[i][2],
                                               cookTime=modeDaultValChg[i][0])

            time.sleep(5)
            self.getPreseRecipeDault = commonFunc().commMethodApi(method="getPresetRecipe")

        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"], e)

        for i in  range(len(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"])):
            print(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i], i)
            self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["tempUnit"], "c")

            if json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["tempUnit"] == "c":
                if json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Toast":
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["level"], modeDaultValChg["Toast"][2])

                # elif json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "AirFry" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Reheat" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Roast" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Bake" \
                #         or json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"] == "Broil":
                #     print("AirFry/Reheat/Roast/Bake/Broil/不支持修改默认值")
                #     self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                #         modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                #
                #     self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                #         modeDaultVal[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][2])

                else:
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookSetTime"],
                                     modeDaultValChg[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][0])
                    self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["cookTemp"],
                                     modeDaultValChg[json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["mode"]][2])

            else:
                self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"]["menu"][i]["tempUnit"], "c")


if __name__ == "__main__":
    unittest.main(verbosity=1)
