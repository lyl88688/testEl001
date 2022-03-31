# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、
#描述：
#==================================================


import unittest,ddt
from lib.mcuAndWifi import *


#全局变量
opCode = 0xA3E7

testData = [60, 1200]

# 应答数据,无应答数据，为空字典，有数据与testData格式一致。
responseData = {

}

@ddt.ddt
#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        time.sleep(5)
        opCode = 0xA405

        testData = {"name1": [1, 17],
                    "name2": [1, 2],
                    "name3": [1, 1],
                    "name4": [4, 0],
                    "name5": [2, 100],
                    "name6": [4, 1800],
                    "name7": [4, 0],
                    "name8": [2, 0]}

        receiveData = opCodeClass().sendAndReceiveData(opCode, testData, responseData)
        time.sleep(10)


    def tearDown(self):
        print("环境恢复。。。。")
        time.sleep(10)
        opCodeClass().rebootMcu()

    @ddt.data(*testData)
    def testMcuAndWifi(self, i):
        testData = {"name1": [1, 4],
                    "name2": [1, 1],
                    "name3": [4, i]}
        try:
            receiveData = opCodeClass().sendAndReceiveData(opCode, testData, responseData)
            exceptData = opCodeClass().resultData(opCode, responseData)

            self.assertEqual(receiveData, exceptData)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


