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
opCode = 0xA40C

testData = {}

# 应答数据,无应答数据，为空字典，有数据与testData格式一致。
responseData = {"name1":[1,1],
                "name2":[1,11],
                "name3":[1,0],
                "name4":[1,2],
                "name5":[2,390],
                "name6":[4,1200],
                "name7":[4,0],
                "name18":[1,0],
                "name14":[1,1],
                "name15":[2,400],
                "name16":[4,480],
                "name17":[4,0],
                "name28":[1,0],
                "name24": [1, 3],
                "name25": [2, 375],
                "name26": [4, 480],
                "name27": [4, 0],
                "name38": [1, 0],
                "name34": [1, 36],
                "name35": [2, 385],
                "name36": [4, 360],
                "name37": [4, 0],
                "name48": [1, 0],
                "name44": [1, 6],
                "name45": [2, 385],
                "name46": [4, 1200],
                "name47": [4, 0],
                "name58": [1, 0],
                "name54": [1, 5],
                "name55": [2, 395],
                "name56": [4, 720],
                "name57": [4, 0],
                "name68":[1,0],
                "name64":[1,17],
                "name65":[2,360],
                "name66":[4,600],
                "name67":[4,0],
                "name78":[1,0],
                "name74": [1, 35],
                "name75": [2, 350],
                "name76": [4, 300],
                "name77": [4, 0],
                "name88": [1, 0],
                "name84": [1, 15],
                "name85": [2, 400],
                "name86": [4, 600],
                "name87": [4, 0],
                "name98": [1, 0],
                "name94": [1, 9],
                "name95": [2, 320],
                "name96": [4, 1200],
                "name97": [4, 0],
                "name108": [1, 0],
                "name104": [1, 16],
                "name105": [2, 400],
                "name106": [4, 600],
                "name107": [4, 0]}


#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        opCode = 0xA2E2
        testData = {"name1": [1, 1]}
        receiveData = opCodeClass().sendAndReceiveData(opCode, testData, responseData)
        time.sleep(5)

    def tearDown(self):
        print("环境恢复。。。。")
        opCodeClass().rebootMcu()
        time.sleep(2)

    def testMcuAndWifi(self):
        try:
            receiveData = opCodeClass().sendAndReceiveData(opCode, testData, responseData)
            exceptData = opCodeClass().resultData(opCode, responseData)

            self.assertEqual(receiveData, exceptData)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


