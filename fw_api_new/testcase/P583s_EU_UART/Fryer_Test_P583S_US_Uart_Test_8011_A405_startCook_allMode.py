# _*_ coding:utf-8 _*_

#==================================================
#
#
#
#步骤
#1、测试最大值、最小值及最小值减阈值（低温不处理判断）
#描述：
#==================================================


import unittest,ddt
from lib.mcuAndWifi import *

#全局变量
opCode = 0xA405

# 应答数据,无应答数据，为空字典，有数据与testData格式一致。
responseData = {}

testData = opCodeClass().allModeData()
print(testData)

modedata = []
m = []
for i in testData :
    # print(i["mode"])
    if i["mode"] == "Veggies":
        m.append([0x07,i["tempDegMin"],i['timeMax']*60])
        m.append([0x07,i["tempDegMax"],i['timeMin']*60])
        m.append([0x07,i["tempDegMin"]-5,i['timeMin']*60])
    elif i["mode"] == "Roast":
        m.append([0x0F,i["tempDegMin"],i['timeMax']*60])
        m.append([0x0F,i["tempDegMax"],i['timeMin']*60])
        m.append([0x0F,i["tempDegMin"]-5,i['timeMin']*60])
    elif i["mode"] == "Broil":
        m.append([0x10,i["tempDegMin"],i['timeMax']*60])
        m.append([0x10,i["tempDegMax"],i['timeMin']*60])
        m.append([0x10,i["tempDegMin"]-5,i['timeMin']*60])
    elif i["mode"] == "AirFry":
        m.append([0x11, i["tempDegMin"], i['timeMax'] * 60])
        m.append([0x11, i["tempDegMax"], i['timeMin'] * 60])
        m.append([0x11, i["tempDegMin"]-5, i['timeMin'] * 60])
    elif i["mode"] == "Reheat":
        m.append([0x23,i["tempDegMin"],i['timeMax']*60])
        m.append([0x23,i["tempDegMax"],i['timeMin']*60])
        m.append([0x23,i["tempDegMin"]-5,i['timeMin']*60])
    else:
        m.append([i["recipeId"],i["tempDegMin"],i['timeMax']*60])
        m.append([i["recipeId"],i["tempDegMax"],i['timeMin']*60])
        m.append([i["recipeId"],i["tempDegMin"]-5,i['timeMin']*60])


for n in m:
    modedata.append(n)

print(modedata)


@ddt.ddt
#测试体
class cosoriTest(unittest.TestCase):
    def setUp(self):
        print("环境准备。。。。")
        time.sleep(2)

    def tearDown(self):
        print("环境恢复。。。。")
        opCodeClass().rebootMcu()

    @ddt.data(*modedata)
    #@ddt.unpac
    def testMcuAndWifi(self, i):
        testData = {"name1": [1, 17],
                    "name2": [1, i[0]],
                    "name3": [1, 2],
                    "name4": [4, 0],
                    "name5": [2, i[1]],
                    "name6": [4, i[2]],
                    "name7": [4, 0],
                    "name8": [2, 0]}
        try:
            receiveData = opCodeClass().sendAndReceiveData(opCode, testData, responseData)
            exceptData = opCodeClass().resultData(opCode, responseData)

            self.assertEqual(receiveData, exceptData)

        except Exception as e:
            self.assertEqual(0, e)


if __name__ == "__main__":

    unittest.main(verbosity=1)


