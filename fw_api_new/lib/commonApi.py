#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'eleven'

import os,sys
from requests.packages import urllib3
# 禁用安全请求警告
urllib3.disable_warnings()
sys.path.append(os.path.dirname(__file__))
import requests
import json
from lib.loggingTest import *
from lib import globalName

#全局变量
header = {"Content-Type":"application/json"}
#毫秒级时间戳
traceId = str(int(round(time.time() * 1000)))



class commonFunc():
    def __init__(self):
        self.mode = ""
        self.recipeId = ""
        self.cookTemp = 180
        self.cookTime = 1800
        self.unit = "f"
        self.cookLevel = 4
        self.preheatTemp = 0
        self.enabled = True
        self.data = {}

    def gentoken(self, emailname, pwd,testUrl):
        data_user = {
            "email": emailname,
            "password": pwd,
            "registerTime": 0,
            "isRequiredVerify": True,
            "userType": "1",
            "traceId": "",
            "appVersion": "VeSync 3.0.56",
            "phoneOS": "Android 10",
            "acceptLanguage": "en",
            "method": "login",
            "phoneBrand": "CLT-AL01",
            "timeZone": "America/Phoenix",
            "debugMode": False
        }

        loginRes = requests.post(url = testUrl, headers = header , json = data_user, verify=False)

        return loginRes

    def debugLevel(self, method="setLogLevel", debugMode=globalName.debugModeDef):
        self.commInfo = self.deviceInfo()
        # 后续增加对data数据进行处理，整合所有方法。
        self.data = {"logLevel": "DEBUG", "logRawLevel": debugMode}
        self.commCmd = {"method":method, "data":self.data, "source": "xxx"}
        self.commInfo["payload"] = self.commCmd

        # 增加while目的：由于联调环境不稳定，时常有断链的情况，故增加多次请求，确保发送成功。20210624
        i = 0
        while i <= 2:
            try:
                self.commRes = requests.post(url = globalName.device_url, json = self.commInfo, verify = False)
                if self.data["logRawLevel"] == "DEBUG":
                    print("打开串口模式---->Debug", json.loads(self.commRes.text))
                else:
                    print("关闭串口模式---->Off", json.loads(self.commRes.text))

                return self.commRes
            except Exception as e:
                print("请求响应异常--->%s"%e)
                Logger().getLog().debug("debugLevel 请求响应异常--->%s" % e)
                time.sleep(3)
                i += 1

        Logger().getLog().debug("===================debugLevel 请求响应异常======================")
        return self.commRes

    def getAppDevInfo(self, tk, accountId):
        data = {"traceId": traceId,
                "method": "devices",
                "token": tk,
                "accountID": accountId,
                "timeZone": "timeZone",
                "acceptLanguage": "en",
                "appVersion": "v2.3.2",
                "phoneBrand": "MI8",
                "phoneOS": "android 8.1",
                "pageSize": 100,
                "pageNum": 10
            }
        testUrl = "https://test-online-dev.vesync.com/cloud/v1/deviceManaged/devices"

        self.re = requests.post(url=testUrl, headers=header, json=data, verify=False)

        return self.re

    def deviceInfo(self, method = "bypassV2", configModule="", region="US"):
        while True:
            info = {"acceptLanguage": "en", "accountID":globalName.device_accountID, "appVersion":"2.9.8","cid": globalName.device_cid,
                    "configModule": globalName.device_configModule,"deviceRegion":region,"phoneBrand":"SM-G930F",
                    "phoneOS":"Android 8.0.0", "timeZone":"America/Los_Angeles","token":globalName.device_token,"traceId":traceId,
                    "method":method, "debugMode":False,"payload":""}

            return info

    def commMethodApi(self, method, mode="", recipeId="", cookTemp=180, cookTime=1800, unit="f",cookLevel=4, preheatTemp=0, readyStart=False, enabled=True,
                      pluginName="", versionName="", versionUrl=""):
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
        self.commInfo = self.deviceInfo()
        if method == "setTempUnit":
            self.data = {"unit": unit}

        elif method == "setTimeOrTemp":
            self.data = {"cookSetTime":self.cookTime, "cookTemp":self.cookTemp, "tempUnit":self.unit}

        elif method == "setLightSwitch":
            self.data = {"enabled":self.enabled, "id":1}

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

        self.commCmd = {"method":method, "data":self.data, "source": "APP"}
        self.commInfo["payload"] = self.commCmd

        if method == "getFirmwareUpdateInfoList":
            self.commInfo["cidList"] = [globalName.device_cid]
        else:
            pass

        Logger().getLog().debug(" commMethodApi 发送数据--> %s" % self.commInfo)
        try:
            self.commRes = requests.post(url = globalName.device_url, json = self.commInfo, verify = False)
            Logger().getLog().debug(json.loads(self.commRes.text))
            return self.commRes
        except Exception as e:
            Logger().getLog().error("commMethodApi 请求响应异常--->%s" % e)


    def commMethodApiNew(self, method, mode="", recipeId="", cookTemp=180, cookTime=1800, unit="f",cookLevel=4, preheatTemp=0, readyStart=False):
        """
        提高效率：将常用开始、获取状态和结束函数从commMethodApi分离出来，提高测试效率。
        将接口进行封装，避免接口函数过多，增加维护量。
        :param mode: 模式
        :param recipeId: 菜单ID
        :param unit: 温度单位
        :param cookTemp: 温度值
        :param cookTime: 烹饪时间
        暂支持method：{"method": "startCook,getOvenStatusV2、endCook","data": {}, "source": "xxx"}
        """
        self.commInfo = self.deviceInfo()
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

        else:
            self.data = {}

        self.commCmd = {"method": method, "data": self.data, "source": "xxx"}
        self.commInfo["payload"] = self.commCmd
        # Logger().getLog().debug(" commMethodApiNew 发送数据--> %s" % self.commInfo)
        try:
            if method == "endCook":
                n = 0
                self.commRes = requests.post(url=globalName.device_url, json=self.commInfo, verify=False)
                while method == "endCook" and json.loads(self.commRes.text)["result"]["code"] != 0 and         \
                        json.loads(self.commRes.text)["result"]["code"] != 11903000 and n < 3:
                    if json.loads(self.commRes.text)["result"]["code"] == 11005000:
                        return self.commRes
                    else:

                        Logger().getLog().debug("请求停止烹饪失败--->%s" % json.loads(self.commRes.text)["result"]["code"])
                        time.sleep(2)
                        n += 1
                        self.commRes = requests.post(url=globalName.device_url, json=self.commInfo, verify=False)
            else:
                self.commRes = requests.post(url=globalName.device_url, json=self.commInfo, verify=False)
                return self.commRes

        except Exception as e:
            Logger().getLog().error("commMethodApiNew 请求响应异常--->%s" % e)

    def getVersionInfo(self, typeVer="", versionVal=""):
        """
        获取设备版本信息
        typeVer:mainFw/mcuFw
        versionVal:升级版本号
        :return:
        {'traceId': '1622125013777', 'code': 0, 'msg': '请求成功', 'result': {'cidFwInfoList': [{'deviceCid': 'vssk71cf13094f6ab9194e357687e642', 'deviceName': 'cs100',
        'deviceImg': 'https://image.vesync.com/defaultImages/CS100_AO_Series/img_cs100_160.png', 'uuid': 'f239f2cb-689d-4a40-bef3-7661a197b4bc',
        'configModule': 'WiFiBTOnboardingNotify_Oven_CS100-AO_US', 'connectionType': 'WiFi+BTOnboarding+BTNotify', 'macID': '40:f5:20:87:90:ee', 'deviceRegion': 'US',
        'code': 0, 'msg': None, 'firmUpdateInfos': [{'upgradeLevel': 10, 'latestVersionUrl': 'http://54.222.135.96:4005/firm/amazon/WiFiBTOnboardingNotify_Oven_CS100-AO_US/mcuFw-C2/v2.0.13/CS100_MCU_C2_US_ota_v2.0.13.bin', 'partFirmwareVersionUrl': '',
        'currentVersion': '2.0.10', 'latestVersion': '2.0.13', 'releaseNotes': '2.0.13', 'pluginName': 'mcuFw-C2', 'priority': 0, 'upgradeTimeoutInSec': 120, 'isMainFw': False},
        {'upgradeLevel': 0, 'latestVersionUrl': None, 'partFirmwareVersionUrl': None, 'currentVersion': '1.2.01', 'latestVersion': None, 'releaseNotes': None, 'pluginName': 'mainFw', 'priority': 1, 'upgradeTimeoutInSec': 120, 'isMainFw': True}]}], 'macIDFwInfoList': None}}
        """
        self.getFirmwareUpdateInfoListUrl = "https://test-online-dev.vesync.com/cloud/v2/deviceManaged/getFirmwareUpdateInfoList"

        self.getVerInfo = self.deviceInfo(method = "getFirmwareUpdateInfoList")
        self.getVerInfo["cidList"] = [globalName.device_cid]    #需要查询的设备，以列表形式传入。

        time.sleep(120)
        i = 0
        currentVer = ""
        #增加while目的：由于联调环境不稳定，时常有断链的情况，故增加多次请求，确保发送成功。20210510

        while i < 18 and versionVal != currentVer:
            try:
                self.getVersionRes = requests.post(url = self.getFirmwareUpdateInfoListUrl, headers=header, json = self.getVerInfo, verify = False)
                #当前版本号json.loads(getVersionRes.tex t)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"]
                Logger().getLog().debug(json.loads(self.getVersionRes.text))
                if "mcuFw" in typeVer:
                    currentVer = json.loads(self.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"]
                elif "mainFw" in typeVer:
                    currentVer = json.loads(self.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"]
                else:
                    Logger().getLog().error("pluginName有误。。。。。。。")
                    print("pluginName有误。。。。。。。")

                Logger().getLog().error("versionVal = %s----------currentVer = %s"%(versionVal, currentVer))
                time.sleep(10)
                i += 1

            except:
                time.sleep(10)
                Logger().getLog().error("getVersionInfo 请求响应异常--->%s"%i)
                i += 1

            try:
                print("获取当前MCU版本号--->%s"%(json.loads(self.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"]))
                print("获取当前WIFI版本号--->%s"%(json.loads(self.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][1]["currentVersion"]))
            except:
                #防止部分单品只有mcu，没有wifi
                print("获取当前MCU版本号--->%s" % (json.loads(self.getVersionRes.text)["result"]["cidFwInfoList"][0]["firmUpdateInfos"][0]["currentVersion"]))

        return self.getVersionRes

    def getreportFirmUpV2(self ,pluginName="mainFw"):
        """
        接口地址: /cloud/v1/deviceManaged/getFirmwareStatusList
        :return:
        """
        url = "https://test-online.vesync.com/cloud/v1/deviceManaged/getFirmwareStatusList"
        param = {
            "traceId": traceId,
            "acceptLanguage": "en",
            "method":"getFirmwareStatusList",
            "appVersion": "2.4.3(build 20)",
            "phoneBrand": "NX609J",
            "phoneOS": "Android",
            "token": globalName.device_token,
            "timeZone": "Asia/Shanghai",
            "accountID": globalName.device_accountID,
            "debugMode": False,
            "cidInfoList": [{"cid":globalName.device_cid, "pluginName":pluginName}]
        }
        i = 0
        while i < 3:
            try:
                self.firmUpRes = requests.post(url=url, json=param, verify=False)
                Logger().getLog().debug(json.loads(self.firmUpRes.text))
                m = 0
                while json.loads(self.firmUpRes.text)["result"]["statusList"][0]["updateStatus"] == 17 and m < 1:
                    print("固件下载失败。。。。。。失败状态码：%s"%json.loads(self.firmUpRes.text)["result"]["statusList"][0]["updateStatus"])

                    return self.firmUpRes
                else:
                    m += 1
                i += 1
            except:
                time.sleep(3)
                i += 1
                Logger().getLog().error(" getreportFirmUpV2 请求响应异常--> %s"%i)

    def errCode(self, codeNo):
        if codeNo == 0:
            pass
        elif codeNo == 11005000:
            print("设备处于待机状态")
        elif codeNo == 11903000:
            print("设备未处于烹饪状态,无需关闭。")
        elif codeNo == 11010000:
            print("超过温度上限错误")
        elif codeNo == 11011000:
            print("超过温度下限错误")
        elif codeNo == 11008000:
            print("时长范围超过上限错误")
        elif codeNo == 11009000:
            print("时长范围超过下限错误")
