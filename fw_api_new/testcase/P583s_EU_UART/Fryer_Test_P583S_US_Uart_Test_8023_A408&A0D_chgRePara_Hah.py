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
opCode = 0xA40B
opCode1 = 0xA40D


testData = [1,2,3,5,6,9,17,35,15,16,36]
# 应答数据,无应答数据，为空字典，有数据与testData格式一致。


@ddt.ddt
#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        time.sleep(3)

    def tearDown(self):
        print("环境恢复。。。。")
        time.sleep(3)
        opCodeClass().rebootMcu()

    @ddt.data(*testData)

    def testMcuAndWifi(self,i):
        if i == 1:
            #175-400 400 8  1-20  80-205  205
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 330],
                              "name4": [4, 600],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 2:
            #350-400 390 20  1-60   175-205 200
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 360],
                              "name4": [4, 660],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 3:
            #320-400 375 8  1-30  160-205 190
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 325],
                              "name4": [4, 720],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 5:
            #350-400  395 12  1-20   175-205 200
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 355],
                              "name4": [4, 780],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 6:
            #350-400 38  12  1-60  175-205  195
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 365],
                              "name4": [4, 840],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 7:
            #320-400 385  6   1-30   160-205
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 370],
                              "name4": [4, 900],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 9:
            #250-400  320  20  1-60  175-205  160
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 255],
                              "name4": [4, 960],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 15:
            #175-400 400 10 1-60 80-205 205
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 180],
                              "name4": [4, 1020],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 16:
            #350-400 400 10 1-30 175-205 205
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 365],
                              "name4": [4, 1080],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 17:
            #175-400 360 10 1-60 80-205 180
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 190],
                              "name4": [4, 1140],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 35:
            #300-400 350 5 1-15 150-205 1775
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 305],
                              "name4": [4, 720],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1
        elif i == 36:
            #320-400 385 6 1-30 160-205 195
            self.testData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 325],
                              "name4": [4, 720],
                              "name5": [4, 0]}

            self.responseData1 = self.testData1

        try:
            receiveData = opCodeClass().sendAndReceiveData(opCode, self.testData1, self.responseData1)
            exceptData = opCodeClass().resultData(opCode, self.responseData1)

            self.assertEqual(receiveData, exceptData)

        except Exception as e:
            self.assertEqual(0, e)

    @ddt.data(*testData)
    def testMcuAndWifi1(self,i):
        self.testData1 = {"name1": [1, i]}
        if i == 1:
            #175-400 400 8  1-20  80-205  205
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 400],
                              "name4": [4, 480],
                              "name5": [4, 0]}

        elif i == 2:
            #350-400 390 20  1-60   175-205 200
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 390],
                              "name4": [4, 1200],
                              "name5": [4, 0]}

        elif i == 3:
            #320-400 375 8  1-30  160-205 190
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 375],
                              "name4": [4, 480],
                              "name5": [4, 0]}

        elif i == 5:
            #350-400  395 12  1-20   175-205 200
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 395],
                              "name4": [4, 720],
                              "name5": [4, 0]}

        elif i == 6:
            #350-400 385  200  1-60  175-205  195
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 385],
                              "name4": [4, 1200],
                              "name5": [4, 0]}

        elif i == 7:
            #320-400 385  6   1-30   160-205
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 385],
                              "name4": [4, 360],
                              "name5": [4, 0]}

        elif i == 9:
            #250-400  320  20  1-60  175-205  160
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 320],
                              "name4": [4, 1200],
                              "name5": [4, 0]}

        elif i == 15:
            #175-400 400 10 1-60 80-205 205
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 400],
                              "name4": [4, 600],
                              "name5": [4, 0]}

        elif i == 16:
            #350-400 400 10 1-30 175-205 205
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 400],
                              "name4": [4, 600],
                              "name5": [4, 0]}

        elif i == 17:
            #175-400 360 10 1-60 80-205 180
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 360],
                              "name4": [4, 600],
                              "name5": [4, 0]}

        elif i == 35:
            #300-400 350 5 1-15 150-205 1775
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 350],
                              "name4": [4, 300],
                              "name5": [4, 0]}


        elif i == 36:
            #320-400 385 6 1-30 160-205 195
            self.responseData1 = {"name1": [1, 1],
                              "name2": [1, i],
                              "name3": [2, 385],
                              "name4": [4, 360],
                              "name5": [4, 0]}


        try:
            receiveData = opCodeClass().sendAndReceiveData(opCode1, self.testData1, self.responseData1)
            exceptData = opCodeClass().resultData(opCode1, self.responseData1)

            self.assertEqual(receiveData, exceptData)

        except Exception as e:
            self.assertEqual(0, e)

if __name__ == "__main__":

    unittest.main(verbosity=1)


