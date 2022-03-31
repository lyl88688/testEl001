# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#
#描述：状态
#==================================================


import unittest, requests,time
from lib.commonData import *
import json,ddt,random


#全局变量



#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        commonFunc().commMethodApiNew(method="endCook")


    def tearDown(self):
        pass


    def testStatusStandby(self):
        print("=================开始测试=====================")
        try:
            print("======cooking=========")
            modeCookMode = "Roast"
            exceptMode = "Roast"  # 测试模式
            modeCookrecipeId = 13  # 对应菜单
            exceptRecipeType = 3  # 对应菜单类型
            resCook = commonFunc().commMethodApiNew(method="startCook",mode=modeCookMode, recipeId=modeCookrecipeId, unit = "f")
            time.sleep(5)

            print("======standby=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

            time.sleep(2)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "standby")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)


    def testStatusCooking(self):
        print("=================开始测试=====================")
        try:
            print("======cooking=========")
            modeCookMode = "Roast"
            exceptMode = "Roast"  # 测试模式
            modeCookrecipeId = 13  # 对应菜单
            exceptRecipeType = 3  # 对应菜单类型
            resCook = commonFunc().commMethodApiNew(method="startCook",mode=modeCookMode, recipeId=modeCookrecipeId, unit = "f")

            time.sleep(2)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "cooking")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")


    def testStatusCookStop(self):
        print("=================开始测试=====================")
        try:
            print("======cookStop=========")
            modeCookMode = "Roast"
            exceptMode = "Roast"  # 测试模式
            modeCookrecipeId = 13  # 对应菜单
            exceptRecipeType = 3  # 对应菜单类型
            resCook = commonFunc().commMethodApiNew(method="startCook",mode=modeCookMode, recipeId=modeCookrecipeId, unit = "f")

            time.sleep(5) #防止频繁操作
            self.pauseWorkStatus = commonFunc().commMethodApi(method="pauseWork")

            time.sleep(2)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "cookStop")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def testStustaCookend(self):
        print("=================开始测试=====================")
        try:
            modeCookMode = "Roast"
            exceptMode = "Roast"  # 测试模式
            modeCookrecipeId = 13  # 对应菜单
            exceptRecipeType = 3  # 对应菜单类型
            cookSetTime = 60
            resCook = commonFunc().commMethodApiNew(method="startCook",mode=modeCookMode, recipeId=modeCookrecipeId, cookTime=cookSetTime,unit = "f")

            time.sleep(80)
            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "cookEnd")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")


    def teststatusReady(self):
        print("=================开始测试=====================")
        try:
            print("======cookStop=========")
            modeCookMode = "Roast"
            exceptMode = "Roast"  # 测试模式
            modeCookrecipeId = 13  # 对应菜单
            exceptRecipeType = 3  # 对应菜单类型
            self.readyRes = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId, readyStart=True)
            time.sleep(5)

            self.resStatus = commonFunc().commMethodApiNew(method="getAirfryerStatus")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "ready")

            commonFunc().commMethodApiNew(method="endCook")
        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.getPreseRecipeDault.text)["result"]["result"], e)

        commonFunc().commMethodApiNew(method="endCook")

if __name__ == "__main__":
    unittest.main(verbosity=1)
