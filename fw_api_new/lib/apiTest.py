#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'eleven'

import os,sys
import requests
import json
from lib.loggingTest import *
from lib import globalName
from lib.commonApi import commonFunc


class interErrVal():
    """
    验证接口异常值，分为string、int、bool验证点。

    """
    def testStringVal(self):
        testStringList = [" ",
                   "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
                   "中文", "~", "!", "@", "#", "$", "%", "^", "&", "*", "（", "）", "—", "+", "=", "{", "}", ":",
                   ";", "'", "<", ">", "?", "/", "\\", 123, False, True, 11.1, 0, -1, 8/3]

        return testStringList

    def testIntVal(self):
        testIntList = [" ",
                   "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
                   "中文", "~", "!", "@", "#", "$", "%", "^", "&", "*", "（", "）", "—", "+", "=", "{", "}", ":",
                   ";", "'", "<", ">", "?", "/", "\\", False, True]

        return testIntList

    def testBoolVal(self):
        testBoolList = [" ",
                   "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
                   "中文", "~", "!", "@", "#", "$", "%", "^", "&", "*", "（", "）", "—", "+", "=", "{", "}", ":",
                   ";", "'", "<", ">", "?", "/", "\\", 123, 11.1, 0, -1, 8/3]

        return testBoolList

    def commMethodApiPaylaod(self, method, mode="", recipeId="", cookTemp=180, cookTime=1800, unit="f",cookLevel=4, preheatTemp=0, readyStart=False, enabled=True,
                      pluginName="", versionName="", versionUrl="", errVal=""):
        """
        将接口进行封装，避免接口函数过多，增加维护量。
        :param mode: 模式
        :param recipeId: 菜单ID
        :param unit: 温度单位
        :param cookTemp: 温度值
        :param cookTime: 烹饪时间
        暂支持method：{"method": "startCook,getOvenStatusV2、confirmCookEnd、preheatCook、endCook、endPreheat、pauseWork、resumeWork、
        updatePresetRecipe、getPresetRecipe、resetAllPresetRecipe、testUart","data": {}, "source": "xxx"}

        ovenUpdatPresetRecipe,(self, recipeMode, recipeCookTemp, recipeCookSetTime, recipeTempUnit='f', level=4)
        {"method": "preheat", "data": {"preheatTemp": 180, "preheatTempUnit": "f"}, "source": "xxx"}
        {"method":"upFirmware", "data":{"pluginName":pluginName, "newVersion":versionName, "url":versionUrl}
        """
        self.commInfo = commonFunc().deviceInfo()
        # 后续增加对data数据进行处理，整合所有方法。
        if method == "startCook":
            self.data = {"accountId": globalName.device_accountID,
                         "readyStart": False,
                         "recipeName": "Bake",
                         "hasPreheat": 0,
                         "tempUnit": "f",
                         "mode": "Bake",
                         "recipeId": 4,
                         "recipeType": 3,
                         "startAct": {"cookSetTime": 1800,
                                      "cookTemp": 150,
                                      "shakeTime": 0,
                                      "level": 4,
                                      "preheatTemp": 0}}
            self.data["mode"] = mode
            self.data["recipeName"] = mode
            self.data["recipeId"] = recipeId
            self.data["readyStart"] = readyStart
            self.data["tempUnit"] = unit
            self.data["startAct"]["cookTemp"] = cookTemp
            self.data["startAct"]["cookSetTime"] = cookTime
            self.data["startAct"]["preheatTemp"] = preheatTemp
            self.data["startAct"]["level"] = cookLevel

        elif method == "setTempUnit":
            self.data = {"unit": unit}

        elif method == "setTimeOrTemp":
            self.data = {"cookSetTime":cookTime, "cookTemp":cookTemp, "tempUnit":unit}

        elif method == "setLightSwitch":
            self.data = {"enabled":enabled, "id":1}

        elif method == "upFirmware":
            self.data = {"pluginName":pluginName, "newVersion":versionName, "url":versionUrl}

        elif method == "preheat":
            self.data = {"preheatTemp": 180, "preheatTempUnit": "f"}

        elif method == "startAppoint":
            self.data = {"mode":"Bake","accountId":globalName.device_accountID,"recipeId":4,"recipeName":"Bake","recipeType":3,"tempUnit":"c","cookSetTime":300,"cookTemp":66,"shakeTime":0,"appointmentTs":180,"windMode":0,"customExpand":{"heatingType":0,"upTubeTemp":150,"downTubeTemp":150}}

        elif method == "updatePresetRecipe":
            self.data = {"mode":mode,"cookTemp":cookTemp,"cookSetTime":cookTime,"tempUnit":unit, "level":cookLevel}

        else:
            self.data = {}

        self.commCmd = {"method":method, "data":self.data, "source": "xxx"}
        self.commInfo["payload"] = self.commCmd

        if method == "getFirmwareUpdateInfoList":
            self.commInfo["cidList"] = [globalName.device_cid]
        else:
            pass

        return self.commInfo


    def apiTest(self, data):
        """
        将组合后的payload传入
        :param data:
        :return:
        """
        i = 0
        while i <= 3:
            try:
                self.commRes = requests.post(url = globalName.device_url, json = data, verify = False)

                print(json.loads(self.commRes.text))

                return self.commRes
            except Exception as e:
                print("请求响应异常--->%s"%e)
                time.sleep(3)
                i += 1

        return self.commRes