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
modeCookMode = "Bake"
modeCookrecipeId= 4

#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        commonFunc().commMethodApi(method="endCook")

    def tearDown(self):
        pass

    def testStatusHeating(self):
        print("=================开始测试=====================")
        try:
            print("======ovenPreheat=========")
            self.statusHeatingRes = commonFunc().commMethodApi(method="preheat")

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")

            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "heating")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def testStatusPreheatEnd(self):
        print("=================开始测试=====================")
        try:
            print("======preheatEnd=========")

            self.statusHeatingRes = commonFunc().commMethodApiNew(method="startCook",mode="Bake", recipeId=4, cookTemp = 180, cookTime = 1800, unit = "f", cookLevel = 4, preheatTemp=180)

            time.sleep(180)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")

            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "preheatEnd")#关联预加热

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")
            # 

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def testStatusHeatStop(self):
        print("=================开始测试=====================")
        try:
            print("======preheatStop=========")
            self.statusHeatingRes = commonFunc().commMethodApi(method="preheat")

            self.pauseWorkStatus = commonFunc().commMethodApi(method="pauseWork")

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "preheatStop")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def testStatusStandby(self):
        print("=================开始测试=====================")
        try:
            print("======standby=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "standby")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)


    def testStatusCooking(self):
        print("=================开始测试=====================")
        try:
            print("======cooking=========")
            modeCookMode = "Bake"
            modeCookrecipeId = 4  # 对应菜单
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId)

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "cooking")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")


    def testStatusCookStop(self):
        print("=================开始测试=====================")
        try:
            print("======cookStop=========")
            modeCookMode = "Bake"
            modeCookrecipeId = 4  # 对应菜单
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId)

            self.pauseWorkStatus = commonFunc().commMethodApi("pauseWork")

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "cookStop")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")


    def testStustaCookend(self):
        print("=================开始测试=====================")
        try:
            print("======startCook=========")
            self.statusHeatingRes = commonFunc().commMethodApi(method="preheat")

            time.sleep(185) #预热为180F,180s，故等待时间大于180s.
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "cookEnd")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def testStatusAppointing(self):
        print("=================开始测试=====================")
        try:
            print("======Appointing=========")
            self.statusAppointingRes = commonFunc().commMethodApi(method="startAppoint")

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "appointing")

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")


    def teststatusReady(self):
        print("=================开始测试=====================")
        try:
            self.readyRes = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId, unit="f", readyStart=True)

            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "ready")

            commonFunc().commMethodApiNew(method="endCook")
        except Exception as e:
            print("=====异常=====", e)
            self.assertEqual(json.loads(self.resStatus.text)["result"]["result"], e)

        commonFunc().commMethodApiNew(method="endCook")

if __name__ == "__main__":
    unittest.main(verbosity=1)
