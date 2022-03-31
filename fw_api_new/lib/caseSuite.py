#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'eleven'

import os,sys
sys.path.append(os.path.dirname(__file__))
from requests.packages import urllib3
# 禁用安全请求警告
urllib3.disable_warnings()
sys.path.append(os.path.dirname(__file__))
from lib.loggingTest import *
from lib.newReport import *
from lib import globalName
from lib.testDataManage import *
from lib.HTMLTestRunner import *


class addRunCase():

    def run_case(self, all_case, result_path=setting.TEST_REPORT):
        """执行所有的测试用例"""
        # 初始化接口测试数据
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filename = result_path + '/' + '自动化测试报告' + now + '.html'
        fp = open(filename,'wb')
        runner = HTMLTestRunner(stream=fp,title='固件测试自动化测试报告',
                                description='MCU版本号：%s  WiFi版本号：%s'%(globalName.newVersionMainFw, globalName.newVersionMcu),
                                tester='COSORI固件测试')

        runner.run(all_case)

        fp.close()
        report = new_report(setting.TEST_REPORT) #调用模块生成最新的报告
        # send_mail(report) #调用发送邮件模块

    def add_case(self, test_path=setting.TEST_CASE):
        """加载所有的测试用例"""
        getTempAndTime().getRegionAndVer()
        Logger().getLog().debug("deviceType --->%s" % globalName.deviceType)
        Logger().getLog().debug(" add_case 单品测试用例路径%s！" % test_path)
        if globalName.deviceType == 0:
            Logger().getLog().debug("device_configModule --->%s" % globalName.device_configModule)
            if  globalName.device_configModule == "WFON_AFR_CAF-P583S-KUS_US":
                discover = unittest.defaultTestLoader.discover(test_path, pattern='FRYER_Test_1.py', top_level_dir=None)

            elif globalName.device_configModule == "VS_WFON_AFR_CAF-P583S-KEU_ONL_EU":
                discover = unittest.defaultTestLoader.discover(test_path, pattern='COSORI_FRYER_P583S_EU_Test_T*.py', top_level_dir=None)

            else:
                Logger().getLog().debug(" add_case 单品选择有误，请重新选择！")

        elif globalName.deviceType == 1:
            if globalName.device_configModule == "WiFiBTOnboardingNotify_Oven_CS100-AO_US":
                discover = unittest.defaultTestLoader.discover(test_path, pattern='OVEN_Test_Timer.py')
            else:
                discover = unittest.defaultTestLoader.discover(test_path, pattern='Oven_Test_Temp_Deg.py',top_level_dir=None)
        else:
            Logger().getLog().debug(" add_case 设备类型有误，重新选择！！！！")

        return discover
