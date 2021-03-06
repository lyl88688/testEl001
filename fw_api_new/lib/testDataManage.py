#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
处理不同设备得测试数据：时间、华氏度、摄氏度及全局变量赋值

"""


import os,sys,random
sys.path.append(os.path.dirname(__file__))
from requests.packages import urllib3
# 禁用安全请求警告
urllib3.disable_warnings()
sys.path.append(os.path.dirname(__file__))
from config import setting
import configparser
from lib.mainWidget import *
from lib import globalName


class getTempAndTime():
    def getTempFah(self, minTemp, maxTemp):
        cookTempFah = []
        i = minTemp
        while i <= maxTemp:
            cookTempFah.append(i)
            i += 5
        else:
            pass

        #增加超边界测试值
        cookTempFah.append(minTemp - 5)
        cookTempFah.append(maxTemp + 5)

        return cookTempFah

    def getTempDeg(self, minTemp, maxTemp):
        cookTempDeg = []
        cookSetTempdeg = [27, 29, 32, 35, 38, 41, 43, 46, 49, 52, 54, 57, 60, 63,
                          66, 68, 71, 74, 77, 79, 82, 85, 88, 91, 93,96, 99, 102, 104,
                          107, 110, 113, 116, 118, 121, 124, 127, 129, 132, 135, 138,
                          141, 143, 146,149,152, 154, 157, 160, 163, 166, 168, 171, 174,
                          177, 179, 182, 185, 188, 191, 193, 196, 199, 202, 204,207, 210,
                          213, 216, 218, 221, 224, 227, 229, 232]
        for i in cookSetTempdeg:
            if minTemp <= i <= maxTemp:
                cookTempDeg.append(i)
            else:
                pass

        #增加超边界测试值
        cookTempDeg.append(minTemp - 1)
        cookTempDeg.append(maxTemp + 1)

        return cookTempDeg

    def getFryerTempDeg(self, minTemp, maxTemp):
        cookFryerTempDeg = []
        i = minTemp
        if globalName.device_configModule == "WFON_AFR_CAF-P583S-KUS_US" or globalName.device_configModule == "VS_WFON_AFR_CAF-P583S-KEU_ONL_EU":
            while i <= maxTemp:
                cookFryerTempDeg.append(i)
                i += 5
        else:
            cookSetTempdeg = [27, 29, 32, 35, 38, 41, 43, 46, 49, 52, 54, 57, 60, 63,
                              66, 68, 71, 74, 77, 79, 82, 85, 88, 91, 93, 96, 99, 102, 104,
                              107, 110, 113, 116, 118, 121, 124, 127, 129, 132, 135, 138,
                              141, 143, 146, 149, 152, 154, 157, 160, 163, 166, 168, 171, 174,
                              177, 179, 182, 185, 188, 191, 193, 196, 199, 202, 204, 207, 210,
                              213, 216, 218, 221, 224, 227, 229, 232]
            for i in cookSetTempdeg:
                if minTemp <= i <= maxTemp:
                    cookFryerTempDeg.append(i)
                else:
                    pass

        # 增加超边界测试值
        cookFryerTempDeg.append(minTemp - 5)
        cookFryerTempDeg.append(maxTemp + 5)

        return cookFryerTempDeg

    def getTime(self, minTime, maxTime, mode = "", temp=350):
        cookTime = []
        t = minTime
        while t < maxTime:
            if mode == "" and t <= maxTime:
                if t <= 60:
                    cookTime.append(t*60)
                    t += 1
                elif 60 < t <= 120:
                    cookTime.append(t*60)
                    t +=  5
            elif mode == "Fermentation" and t <= maxTime:
                cookTime.append(t*60)
                t += 30

            elif mode == "Dehydrate" and t <= maxTime:
                cookTime.append(t*60)
                t += 30

            elif mode == "SlowCook" and t <= maxTime:
                cookTime.append(t*60)
                t += 30

            else:
                if t <= 60:
                    cookTime.append(t * 60)
                    t += 1
                elif 60 < t <= 120:
                    cookTime.append(t * 60)
                    t += 5

        if minTime < 60 :
            if mode == "Fermentation" or mode == "Dehydrate" or mode == "SlowCook":
                cookTime.append((minTime - 30) * 60)
            else:
                cookTime.append((minTime - 1)*60)


        if maxTime <= 60:
            cookTime.append((maxTime + 1)*60)
        elif 60 < maxTime <= 120:
            cookTime.append((maxTime + 5)*60)
        elif maxTime > 400:
            cookTime.append((maxTime + 30) * 60)


        # cookTimeTest1 = cookTime[-10:]#确保离点值在测试范围内
        # random.shuffle(cookTime)#将测试数据随机排
        # cookTimeTest2 = cookTime[0:len(cookTime)//3]#测试数据1/3
        # newCookTime = cookTimeTest1 + cookTimeTest2
        # return newCookTime

        return cookTime


    def getData(self, dataType):
        #根据测试数据类型，生成对应测试集。
        # 获取ini数据
        con = configparser.ConfigParser()
        con.read(setting.TEST_CONFIG, encoding='utf-8')
        testDevice = globalName.testDevice
        mode = con.get(testDevice, "mode")
        recipeId = con.get(testDevice, "recipeId")
        timeMin = con.get(testDevice, "timeMin")
        timeMax = con.get(testDevice, "timeMax")
        tempHahMin = con.get(testDevice, "tempHahMin")
        tempHahMax = con.get(testDevice, "tempHahMax")
        tempDegMin = con.get(testDevice, "tempDegMin")
        tempDegMax = con.get(testDevice, "tempDegMax")
        self.newmode = (mode.split(","))
        self.newrecipeId = (recipeId.split(","))
        self.newtimeMin = (timeMin.split(","))
        self.newtimeMax = (timeMax.split(","))
        self.newtempHahMin = (tempHahMin.split(","))
        self.newtempHahMax = (tempHahMax.split(","))
        self.newtempDegMin = (tempDegMin.split(","))
        self.newtempDegMax = (tempDegMax.split(","))


        #获取ini数据
        allIniModeData = []
        for iMode in self.newmode:
            dictData = {}
            dictData["mode"] = iMode
            iModeIndex = self.newmode.index(iMode)
            dictData["recipeId"] = int(self.newrecipeId[iModeIndex])
            dictData["timeMin"] = int(self.newtimeMin[iModeIndex])
            dictData["timeMax"] = int(self.newtimeMax[iModeIndex])
            dictData["tempHahMin"] = int(self.newtempHahMin[iModeIndex])
            dictData["tempHahMax"] = int(self.newtempHahMax[iModeIndex])
            dictData["tempDegMin"] = int(self.newtempDegMin[iModeIndex])
            dictData["tempDegMax"] = int(self.newtempDegMax[iModeIndex])
            allIniModeData.append(dictData)

        logger.debug(allIniModeData)
        cookSetData = []

        for testData in allIniModeData:
            print(testData)
            # dataType:  0--time,1--tempHah;2--tempGeg
            if dataType == 0 and globalName.deviceType == 0:
                testData["testUnit"] = "f"
                self.testAllData = getTempAndTime().getTime(testData["timeMin"], testData["timeMax"])
                random.shuffle(self.testAllData)
                for i in self.testAllData:
                    testDataNew = {}
                    testDataNew["mode"] = testData["mode"]
                    testDataNew["recipeId"] = testData["recipeId"]
                    testDataNew["timeMin"] = testData["timeMin"]
                    testDataNew["timeMax"] = testData["timeMax"]
                    testDataNew["tempHahMin"] = testData["tempHahMin"]
                    testDataNew["tempHahMax"] = testData["tempHahMax"]
                    testDataNew["tempDegMin"] = testData["tempDegMin"]
                    testDataNew["tempDegMax"] = testData["tempDegMax"]
                    testDataNew["testUnit"] = testData["testUnit"]
                    testDataNew["testDataVal"] = i
                    cookSetData.append(testDataNew)

            elif dataType == 1 and globalName.deviceType == 0:
                testData["testUnit"] = "f"
                self.testAllData = getTempAndTime().getTempFah(testData["tempHahMin"], testData["tempHahMax"])
                random.shuffle(self.testAllData)
                for i in self.testAllData:
                    testDataNew = {}
                    testDataNew["mode"] = testData["mode"]
                    testDataNew["recipeId"] = testData["recipeId"]
                    testDataNew["timeMin"] = testData["timeMin"]
                    testDataNew["timeMax"] = testData["timeMax"]
                    testDataNew["tempHahMin"] = testData["tempHahMin"]
                    testDataNew["tempHahMax"] = testData["tempHahMax"]
                    testDataNew["tempDegMin"] = testData["tempDegMin"]
                    testDataNew["tempDegMax"] = testData["tempDegMax"]
                    testDataNew["testUnit"] = testData["testUnit"]
                    testDataNew["testDataVal"] = i
                    cookSetData.append(testDataNew)

            elif dataType == 2 and globalName.deviceType == 0:
                testData["testUnit"] = "c"
                self.testAllData = getTempAndTime().getFryerTempDeg(testData["tempDegMin"], testData["tempDegMax"])
                random.shuffle(self.testAllData)
                for i in self.testAllData:
                    testDataNew = {}
                    testDataNew["mode"] = testData["mode"]
                    testDataNew["recipeId"] = testData["recipeId"]
                    testDataNew["timeMin"] = testData["timeMin"]
                    testDataNew["timeMax"] = testData["timeMax"]
                    testDataNew["tempHahMin"] = testData["tempHahMin"]
                    testDataNew["tempHahMax"] = testData["tempHahMax"]
                    testDataNew["tempDegMin"] = testData["tempDegMin"]
                    testDataNew["tempDegMax"] = testData["tempDegMax"]
                    testDataNew["testUnit"] = testData["testUnit"]
                    testDataNew["testDataVal"] = i
                    cookSetData.append(testDataNew)

            elif dataType == 0 and globalName.deviceType == 1:
                testData["testUnit"] = "f"
                self.testAllData = getTempAndTime().getTime(testData["timeMin"], testData["timeMax"], mode=testData["mode"])
                random.shuffle(self.testAllData)
                for i in self.testAllData:
                    testDataNew = {}
                    testDataNew["mode"] = testData["mode"]
                    testDataNew["recipeId"] = testData["recipeId"]
                    testDataNew["timeMin"] = testData["timeMin"]
                    testDataNew["timeMax"] = testData["timeMax"]
                    testDataNew["tempHahMin"] = testData["tempHahMin"]
                    testDataNew["tempHahMax"] = testData["tempHahMax"]
                    testDataNew["tempDegMin"] = testData["tempDegMin"]
                    testDataNew["tempDegMax"] = testData["tempDegMax"]
                    testDataNew["testUnit"] = testData["testUnit"]
                    testDataNew["testDataVal"] = i
                    cookSetData.append(testDataNew)

            elif dataType == 1 and globalName.deviceType == 1:
                testData["testUnit"] = "f"
                self.testAllData = getTempAndTime().getTempFah(testData["tempHahMin"], testData["tempHahMax"])
                random.shuffle(self.testAllData)
                for i in self.testAllData:
                    testDataNew = {}
                    testDataNew["mode"] = testData["mode"]
                    testDataNew["recipeId"] = testData["recipeId"]
                    testDataNew["timeMin"] = testData["timeMin"]
                    testDataNew["timeMax"] = testData["timeMax"]
                    testDataNew["tempHahMin"] = testData["tempHahMin"]
                    testDataNew["tempHahMax"] = testData["tempHahMax"]
                    testDataNew["tempDegMin"] = testData["tempDegMin"]
                    testDataNew["tempDegMax"] = testData["tempDegMax"]
                    testDataNew["testUnit"] = testData["testUnit"]
                    testDataNew["testDataVal"] = i
                    cookSetData.append(testDataNew)

            elif dataType == 2 and globalName.deviceType == 1:
                testData["testUnit"] = "c"
                self.testAllData = getTempAndTime().getTempDeg(testData["tempDegMin"], testData["tempDegMax"])
                random.shuffle(self.testAllData)
                for i in self.testAllData:
                    testDataNew = {}
                    testDataNew["mode"] = testData["mode"]
                    testDataNew["recipeId"] = testData["recipeId"]
                    testDataNew["timeMin"] = testData["timeMin"]
                    testDataNew["timeMax"] = testData["timeMax"]
                    testDataNew["tempHahMin"] = testData["tempHahMin"]
                    testDataNew["tempHahMax"] = testData["tempHahMax"]
                    testDataNew["tempDegMin"] = testData["tempDegMin"]
                    testDataNew["tempDegMax"] = testData["tempDegMax"]
                    testDataNew["testUnit"] = testData["testUnit"]
                    testDataNew["testDataVal"] = i
                    cookSetData.append(testDataNew)

            else:
                logger.error(" getData 获取数据有误，请排查！！！")

        print("Total testcase number is %d" % len(cookSetData))

        logger.debug(cookSetData)
        return  cookSetData

    def getRegionAndVer(self):
        #根据测试数据类型，生成对应测试集。
        # 获取ini数据
        try:
            con = configparser.ConfigParser()
            con.read(setting.TEST_CONFIG, encoding='utf-8')
            testDevice = globalName.testDevice
            logger.debug("测试设备：%s"%testDevice)
            # --------- 读取config.ini配置文件 ---------------
            globalName.updateTime = con.get(testDevice, "updateTime")
            globalName.deviceRegion = con.get(testDevice, "region")
            globalName.pid = con.get(testDevice, "devicepid")
            globalName.pluginNameMainFw = con.get(testDevice, "pluginNameMainFw")
            globalName.newVersionMainFw = con.get(testDevice, "newVersionMainFw")
            globalName.newVersionUrlMainFw = con.get(testDevice, "newVersionUrlMainFw")
            globalName.pluginNameMcu = con.get(testDevice, "pluginNameMcu")
            globalName.newVersionMcu = con.get(testDevice, "newVersionMcu")
            globalName.newVersionUrlMcu = con.get(testDevice, "newVersionUrlMcu")
            globalName.oldVersionMainFw = con.get(testDevice, "oldVersionMainFw")
            globalName.oldVersionUrlMainFw = con.get(testDevice, "oldVersionUrlMainFw")
            globalName.oldVersionMcu = con.get(testDevice, "oldVersionMcu")
            globalName.oldVersionUrlMcu = con.get(testDevice, "oldVersionUrlMcu")

        except:
            logger.debug(" getRegionAndVer 获取ini配置失败，请排查！！！  config.ini路劲：%s"%setting.TEST_CONFIG)
