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

from lib.testDataManage import *
import json,ddt,unittest,time
from unittestreport import rerun


dataType = 2 #0--time,1--tempHah;2--tempGeg

cookSet = getTempAndTime().getData(dataType=dataType)

# print("testApiTemp_Deg:", cookSet)
#测试时间
timeRun = 300   #运行5min


#测试体
@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        modeEndCook = commonFunc().commMethodApiNew(method="endCook")

    def tearDown(self):
        pass

    @ddt.data(*cookSet)
    #@ddt.unpac
    @rerun(count=3, interval=3)
    def testApiTemp(self, startCookTemp):
        print(time.strftime("%Y-%m-%d %X"))
        print("===================开始测试时间==========================", startCookTemp)
        print("======changeUnit=========")
        degUnit = commonFunc().commMethodApi(method="setTempUnit", unit=startCookTemp["testUnit"])
        time.sleep(1)
        print(startCookTemp["mode"], startCookTemp["recipeId"],
              startCookTemp["testUnit"], startCookTemp["timeMin"],"测试值testDataVal: %s"%startCookTemp["testDataVal"],)
        if  startCookTemp["tempDegMin"] <= startCookTemp["testDataVal"] <= startCookTemp["tempDegMax"]:
            try:
                print("======resCook=========", startCookTemp["testUnit"] )
                resCook = commonFunc().commMethodApiNew(method="startCook", mode=startCookTemp["mode"],
                                                        recipeId=startCookTemp["recipeId"],
                                                        cookTime=startCookTemp["timeMin"]+timeRun,
                                                        unit=startCookTemp["testUnit"],
                                                        cookTemp=startCookTemp["testDataVal"])
                self.assertEqual(json.loads(resCook.text)["code"], 0)

                print("======resStatus=========")
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                #测试温度
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["cookTemp"],
                                 startCookTemp["testDataVal"])
                # 测试模式
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["mode"],
                                 startCookTemp["mode"])

                print("======stopCook=========")
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

            except Exception as e:
                print("=====异常=====", e)
                #防止下发成功，但因网络导致无返回。
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"][0]["cookTemp"], startCookTemp["testDataVal"])
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

        else:
            try:
                if startCookTemp["testDataVal"] < startCookTemp["tempDegMin"]:
                    print("温度下限")
                    resCook1 = commonFunc().commMethodApiNew(method="startCook", mode=startCookTemp["mode"],
                                                            recipeId=startCookTemp["recipeId"],
                                                            cookTime=startCookTemp["timeMin"]+timeRun,
                                                            unit=startCookTemp["testUnit"],
                                                            cookTemp=startCookTemp["testDataVal"])
                    #温度下限
                    self.assertEqual(json.loads(resCook1.text)["result"]["code"], 11011000)

                    self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                    self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "standby")
                elif startCookTemp["testDataVal"] > startCookTemp["tempDegMax"]:
                    print("温度上限")
                    resCook2 = commonFunc().commMethodApiNew(method="startCook", mode=startCookTemp["mode"],
                                                            recipeId=startCookTemp["recipeId"],
                                                            cookTime=startCookTemp["timeMin"]+timeRun,
                                                            unit=startCookTemp["testUnit"],
                                                            cookTemp=startCookTemp["testDataVal"])
                    # 温度上限
                    self.assertEqual(json.loads(resCook2.text)["result"]["code"], 11010000)

                    self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                    self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["cookStatus"], "standby")

                modeEndCook = commonFunc().commMethodApiNew(method="endCook")

            except Exception as e:
                print("=====异常=====")
                # 防止下发成功，但因网络导致无返回。
                self.resStatus = commonFunc().commMethodApiNew(method="getOvenStatusV2")
                self.assertEqual(json.loads(self.resStatus.text)["result"]["result"]["stepArray"], e)
                modeEndCook = commonFunc().commMethodApiNew(method="endCook")


if __name__ == "__main__":

    unittest.main(verbosity=1)
