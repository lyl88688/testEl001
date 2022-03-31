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
from lib import loggingTest
import json,ddt,random


#全局变量

exceptModeResult = "Toast"  #测试模式
modeCookMode = "Toast"
modeCookrecipeId = 1  #对应菜单
exceptCodeResult = 0  # 预期结果
testMinModeval = 1 #支持最小模式
testMaxModeval = 7 #支持最大模式

cookSetCookMode = [0, 1, 2, 3, 4, 5, 6, 7, 8]



#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        # log = loggingTest.Logger("CS100TestResult.log", level = "debug")
        commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        pass

    def testMode(self):
        print("=================开始测试模式下发=====================")
        try:
            print("======resCook=========")
            resCook = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(resCook.text)["code"], exceptCodeResult)

            print("======resStatus=========")
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            
            self.assertEqual(json.loads(self.resStatus.text)['result']["result"]['stepArray'][0]['mode'], exceptModeResult)
            # self.assertEqual(json.loads(self.resStatus.text)['result']["result"]['shakeStatus'], 0)  #检查shake状态是否默认0-非默认，1-默认

            print("======stopCook=========")
            modeEndCook = commonFunc().commMethodApiNew(method="endCook")
            

        except Exception as e:
            print("=====异常=====", e)
            self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
            self.assertEqual(json.loads(self.resStatus.text)['result']["result"]['stepArray'][0]['mode'], exceptModeResult)

            modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    @ddt.data(*cookSetCookMode)
    #@ddt.unpac
    def testApiDeg(self, cookModeId):
        print("===================开始测试==========================", cookModeId)

        if testMinModeval <= cookModeId <= testMaxModeval:
            try:
                print("======resCook=========")
                resCook = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId, cookLevel = cookModeId)
                
                self.assertEqual(json.loads(resCook.text)["result"]["code"], exceptCodeResult)

                print("======resStatus=========")
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["level"], cookModeId)

                print("======stopCook=========")
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")
                

            except Exception as e:
                print("=====异常=====", e)
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["level"], cookModeId)

                modeEndCook = commonFunc().commMethodApiNew(method="endCook")
        else:
            try:
                resCook = commonFunc().commMethodApiNew(method="startCook", mode=modeCookMode, recipeId=modeCookrecipeId, cookLevel = cookModeId)
                self.assertEqual(json.loads(resCook.text)["result"]["code"], 11000000)
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"], [])

                modeEndCook = commonFunc().commMethodApiNew(method="endCook")
            except Exception as e:
                print(e)
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"], e)

                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

if __name__ == "__main__":
    unittest.main(verbosity=1)
