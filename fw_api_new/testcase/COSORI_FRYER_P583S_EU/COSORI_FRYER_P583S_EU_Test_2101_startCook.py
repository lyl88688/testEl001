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
import json, ddt

modeCookMode = "Roast"
exceptMode = "Roast"  #测试模式
exceptRecipeId = 13  #对应菜单
exceptRecipeType = 3  #对应菜单类型
exceptCodeResult = 0  # 预期结果
exceptTestFahval = 180
exceptTestDegval = 150
exceptTestTime = 1800
method = "startCook"



testStringData = interErrVal().testStringVal()
testIntgData = interErrVal().testIntVal()
testBoolData = interErrVal().testBoolVal()

testStringParam = ["mode", "accountId", "recipeName", "tempUnit"]
testIntParam = ["recipeId", "recipeType", "hasPreheat", "preheatTemp", "cookSetTime", "cookTemp", "shakeTime" ]

testAllParam = testStringParam + testIntParam

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        commonFunc().commMethodApiNew(method="endCook")
        degUnit = commonFunc().commMethodApi(method="setTempUnit", unit="f")

    def tearDown(self):
        print("环境恢复。。。。")

    @ddt.data(*testStringData)
    #@ddt.unpac
    def testInterFace_string(self, testVal):
        # (self, method, mode
        #  ="", recipeId="", cookTemp=180, cookTime=1800, unit="f", cookLevel=4, preheatTemp=0, readyStart=False, enabled=True,
        #  pluginName="", versionName="", versionUrl="")
        """
        {'acceptLanguage': 'en', 'accountID': '1516480', 'appVersion': '2.9.8', 'cid': 'vsske4aab0074088a8bd78c04e21ced3', 'configModule': 'WiFiBTOnboardingNotify_Oven_CS100-AO_US', 'deviceRegion': 'US', 'phoneBrand': 'SM-G930F', 'phoneOS': 'Android 8.0.0', 'timeZone': 'America/Los_Angeles', 'token': 'rpFG4rNmcD09NbY6VAw6CP4ySiUIluY4UiArY-W50mKmPXBH7w==', 'traceId': '1629342286', 'method': 'bypassV2', 'debugMode': False,
        'payload': {'method': 'startCook', 'data': {'accountId': '1516480', 'readyStart': False, 'recipeName': 'Roast', 'hasPreheat': 0, 'tempUnit': 'f', 'mode': 'Roast', 'recipeId': 13, 'recipeType': 3,
        'startAct': {'cookSetTime': 1800, 'cookTemp': 80, 'shakeTime': 0, 'level': 4, 'preheatTemp': 0}}, 'source': 'xxx'}}
        :param testVal:
        :return:
        """
        try:
            for i in testStringParam:
                print("======================%s======================"%i)
                if type(testVal) == str:
                    testInterfaceData = interErrVal().commMethodApiPaylaod(method=method, mode=modeCookMode, recipeId=exceptRecipeId,
                                                                           cookTemp=exceptTestFahval, cookTime=exceptTestTime)

                    testInterfaceData["payload"]["data"][i] = testVal

                    print(testInterfaceData["payload"]["data"])
                    self.errRes = interErrVal().apiTest(testInterfaceData)

                    #项目中不支持的字段，不需要校验值数据。
                    if i == "accountId" or i == "recipeName":
                        self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 0)
                    else:
                        self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 11000000)

                else:
                    testInterfaceData = interErrVal().commMethodApiPaylaod(method=method, mode=modeCookMode,
                                                                           recipeId=exceptRecipeId,
                                                                           cookTemp=exceptTestFahval,
                                                                           cookTime=exceptTestTime)

                    testInterfaceData["payload"]["data"][i] = testVal

                    print(testInterfaceData["payload"]["data"])
                    self.errRes = interErrVal().apiTest(testInterfaceData)

                    self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 11000000)

                commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            self.assertEqual(e, 0)


    @ddt.data(*testIntgData)
    #@ddt.unpac
    def testInterFace_string(self, testVal):
        # (self, method, mode
        #  ="", recipeId="", cookTemp=180, cookTime=1800, unit="f", cookLevel=4, preheatTemp=0, readyStart=False, enabled=True,
        #  pluginName="", versionName="", versionUrl="")
        """
        {'acceptLanguage': 'en', 'accountID': '1516480', 'appVersion': '2.9.8', 'cid': 'vsske4aab0074088a8bd78c04e21ced3', 'configModule': 'WiFiBTOnboardingNotify_Oven_CS100-AO_US', 'deviceRegion': 'US', 'phoneBrand': 'SM-G930F', 'phoneOS': 'Android 8.0.0', 'timeZone': 'America/Los_Angeles', 'token': 'rpFG4rNmcD09NbY6VAw6CP4ySiUIluY4UiArY-W50mKmPXBH7w==', 'traceId': '1629342286', 'method': 'bypassV2', 'debugMode': False,
        'payload': {'method': 'startCook', 'data': {'accountId': '1516480', 'readyStart': False, 'recipeName': 'Roast', 'hasPreheat': 0, 'tempUnit': 'f', 'mode': 'Roast', 'recipeId': 13, 'recipeType': 3,
        'startAct': {'cookSetTime': 1800, 'cookTemp': 80, 'shakeTime': 0, 'level': 4, 'preheatTemp': 0}}, 'source': 'xxx'}}
        :param testVal:
        :return:
        """
        try:
            for i in testIntParam:
                print("======================%s======================"%i)
                testInterfaceData = interErrVal().commMethodApiPaylaod(method=method, mode=modeCookMode, recipeId=exceptRecipeId,
                                                                       cookTemp=exceptTestFahval, cookTime=exceptTestTime)

                if i == "cookSetTime" or i == "cookTemp" or i == "shakeTime" or i == "preheatTemp":
                    testInterfaceData["payload"]["data"]["startAct"][i] = testVal
                else:
                    testInterfaceData["payload"]["data"][i] = testVal

                print(testInterfaceData["payload"]["data"])
                self.errRes = interErrVal().apiTest(testInterfaceData)

                # 项目中不支持的字段，不需要校验值数据。
                if i == "preheatTemp":
                    self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 0)
                else:
                    self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 11000000)

                commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            self.assertEqual(e, 0)

    @ddt.data(*testAllParam)
    #@ddt.unpac
    def testInterFace_string(self, testVal):
        # (self, method, mode
        #  ="", recipeId="", cookTemp=180, cookTime=1800, unit="f", cookLevel=4, preheatTemp=0, readyStart=False, enabled=True,
        #  pluginName="", versionName="", versionUrl="")
        """
        {'acceptLanguage': 'en', 'accountID': '1516480', 'appVersion': '2.9.8', 'cid': 'vsske4aab0074088a8bd78c04e21ced3', 'configModule': 'WiFiBTOnboardingNotify_Oven_CS100-AO_US', 'deviceRegion': 'US', 'phoneBrand': 'SM-G930F', 'phoneOS': 'Android 8.0.0', 'timeZone': 'America/Los_Angeles', 'token': 'rpFG4rNmcD09NbY6VAw6CP4ySiUIluY4UiArY-W50mKmPXBH7w==', 'traceId': '1629342286', 'method': 'bypassV2', 'debugMode': False,
        'payload': {'method': 'startCook', 'data': {'accountId': '1516480', 'readyStart': False, 'recipeName': 'Roast', 'hasPreheat': 0, 'tempUnit': 'f', 'mode': 'Roast', 'recipeId': 13, 'recipeType': 3,
        'startAct': {'cookSetTime': 1800, 'cookTemp': 80, 'shakeTime': 0, 'level': 4, 'preheatTemp': 0}}, 'source': 'xxx'}}
        :param testVal:
        :return:
        """
        try:
            print("======================%s======================"%testVal)
            testInterfaceData = interErrVal().commMethodApiPaylaod(method=method, mode=modeCookMode, recipeId=exceptRecipeId,
                                                                   cookTemp=exceptTestFahval, cookTime=exceptTestTime)

            if testVal == "cookSetTime" or testVal == "cookTemp" or testVal == "shakeTime" or testVal == "preheatTemp":
                del testInterfaceData["payload"]["data"]["startAct"][testVal]
            else:
                del testInterfaceData["payload"]["data"][testVal]

            self.errRes = interErrVal().apiTest(testInterfaceData)

            # 项目中不支持的字段，不需要校验值数据。
            if testVal == "preheatTemp":
                self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 0)
            else:
                self.assertEqual(json.loads(self.errRes.text)["result"]["code"], 11000000)

            commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            self.assertEqual(e, 0)


if __name__ == "__main__":

    unittest.main(verbosity=1)


