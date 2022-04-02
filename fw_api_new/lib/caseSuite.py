#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
测试的测试集匹配

"""

__author__ = 'eleven'

from lib.newReport import new_report
from lib.testDataManage import *
from lib.HTMLTestRunner import *
import unittest
from lib import globalName

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
        #globalName变量赋值
        getTempAndTime().getRegionAndVer()

        logger.debug(" add_case deviceType --->%s" % globalName.deviceType)
        logger.debug(" add_case 单品测试用例路径%s！" % test_path)

        #炸锅类 deviceType=0
        if globalName.deviceType == 0:
            try:
                logger.debug("device_configModule --->%s" % globalName.device_configModule)
                if  globalName.device_configModule == "WFON_AFR_CAF-P583S-KUS_US":
                    self.discover = unittest.defaultTestLoader.discover(test_path, pattern='Fryer_Test_T*.py', top_level_dir=None)

                elif globalName.device_configModule == "VS_WFON_AFR_CAF-P583S-KEU_ONL_EU":
                    self.discover = unittest.defaultTestLoader.discover(test_path, pattern='COSORI_FRYER_P583S_EU_Test_T*.py', top_level_dir=None)

                else:
                    logger.error(" add_case 单品选择 device_configModule 有误或未添加，请重新选择！")

            except:
                logger.error(" add_case 测试集有误，请排查 pattern 对应名称 ！")

        #烤箱类 deviceType=1
        elif globalName.deviceType == 1:
            try :
                if globalName.device_configModule == "WiFiBTOnboardingNotify_Oven_CS100-AO_US":
                    self.discover = unittest.defaultTestLoader.discover(test_path, pattern='Oven_Test_*.py')

                else:
                    logger.error(" add_case 单品选择 device_configModule 有误或未添加，请重新选择！")

            except:
                logger.error(" add_case 测试集有误，请排查 pattern 对应名称 ！")

        #异常
        else:
            logger.error(" add_case 设备类型 deviceType 有误（非炸锅/烤箱类），重新选择！！！！")

        return self.discover


