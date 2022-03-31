# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、
#描述：
#==================================================


import unittest
from lib.mcuAndWifi import *


#全局变量
opCode = 0xA129

testData = {"name1": [1, 0],
            "name2": [2, 0],
            "name3": [2, 0],
            "name4": [1, 0]}

# 应答数据,无应答数据，为空字典，有数据与testData格式一致。
responseData = {}


#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")

    def tearDown(self):
        print("环境恢复。。。。")

    def testMcuAndWifi(self):
        try:
            receiveData = opCodeClass().sendAndReceiveData(opCode, testData, responseData)
            exceptData = opCodeClass().resultData(opCode, responseData)

            self.assertEqual(receiveData, exceptData)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


