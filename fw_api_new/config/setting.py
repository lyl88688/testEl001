#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os,sys
BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)

urlData = os.path.abspath(os.path.join(os.getcwd(), "..\.."))


# 配置文件
TEST_CONFIG =  os.path.join(BASE_DIR, "", "config\\config.ini")
# 测试用例报告
TEST_REPORT = os.path.join(BASE_DIR, "report")
# 测试用例程序文件
TEST_CASE = os.path.join(BASE_DIR, "testcase")

#
TEST_CONFIG_NEXT =  os.path.join(urlData, "", "config\\config.ini")