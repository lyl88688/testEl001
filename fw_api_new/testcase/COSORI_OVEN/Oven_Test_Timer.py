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


import unittest
from lib.commonData import *
import json,ddt,random

dataType = 0 #0--time,1--tempHah;2--tempGeg
cookSet = getTempAndTime().getData(dataType=dataType)

# print(cookSet)
print("testApiTime")
#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        pass

    @ddt.data(*cookSet)
    #@ddt.unpac
    def testApiTime(self, startCookTime):
        print("===================开始测试时间==========================", startCookTime)
        print("======changeUnit=========")
        degUnit = commonFunc().commMethodApi(method="setTempUnit", unit=startCookTime["testUnit"])
        time.sleep(1)
        print(startCookTime["mode"], startCookTime["recipeId"],
              startCookTime["testUnit"], startCookTime["tempHahMin"],"测试值testDataVal: %s"%startCookTime["testDataVal"])
        if startCookTime["timeMin"]*60 <= startCookTime["testDataVal"] <= startCookTime["timeMax"]*60:
            try:
                print("======resCook=========", startCookTime["testUnit"] )

                resCook = commonFunc().commMethodApiNew(method="startCook", mode=startCookTime["mode"],
                                                        recipeId=startCookTime["recipeId"],
                                                        cookTime=startCookTime["testDataVal"],
                                                        unit=startCookTime["testUnit"],
                                                        cookTemp=startCookTime["tempHahMin"])
                self.assertEqual(json.loads(resCook.text)["code"], 0)

                print("======resStatus=========")
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                #测试温度
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["cookSetTime"],
                                 startCookTime["testDataVal"])
                #测试模式
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["mode"],
                                 startCookTime["mode"])

                print("======stopCook=========")
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

            except Exception as e:
                print("=====异常=====", e)
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["cookSetTime"],
                                 startCookTime["testDataVal"])
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        else:
            try:
                if startCookTime["testDataVal"] < startCookTime["timeMin"]*60:
                    resCook = commonFunc().commMethodApiNew(method="startCook", mode=startCookTime["mode"],
                                                            recipeId=startCookTime["recipeId"],
                                                            cookTime=startCookTime["testDataVal"],
                                                            unit=startCookTime["testUnit"],
                                                            cookTemp=startCookTime["tempHahMin"])
                    #时间超下限
                    if device_configModule == "WiFiBTOnboardingNotify_Oven_CS100-AO_US":
                        #CS100传入0定义为不合法
                        self.assertEqual(json.loads(resCook.text)["result"]["code"], 11000000)
                    else:
                        self.assertEqual(json.loads(resCook.text)["result"]["code"], 11009000)

                    self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                    self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "standby")
                elif startCookTime["testDataVal"] > startCookTime["timeMax"]:
                    resCook = commonFunc().commMethodApiNew(method="startCook", mode=startCookTime["mode"],
                                                            recipeId=startCookTime["recipeId"],
                                                            cookTime=startCookTime["testDataVal"],
                                                            unit=startCookTime["testUnit"],
                                                            cookTemp=startCookTime["tempHahMin"])
                    # 时间超上限
                    self.assertEqual(json.loads(resCook.text)["result"]["code"], 11008000)

                    self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                    self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "standby")

                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

            except Exception as e:
                print("=====异常=====")
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"], e)
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

if __name__ == "__main__":

    unittest.main(verbosity=1)
