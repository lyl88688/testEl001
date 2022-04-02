"""
mcu与wifi之间通讯协议封装

"""



import struct,binascii,time,serial
import configparser
from config import setting
import os
serialCom = "COM19"


class opCodeClass():
    def __init__(self):
        # 定义协议字段
        self.FRAME_HEAD = 0xA5
        # 控制码定义
        self.FRAME_CTR_GET = 0x22
        self.FRAME_CTR_ACK = 0x12
        # 协议版本，当前版本为1
        self.PROTO_VER = 0x01
        # 数据包流水号
        self.seq = 0x41
        # 初始校验和
        self.checkSum = 0
        # 状态码,发送全为0
        self.pStatue = 0x00

        # header（包头）默认长度
        self.headerlen = 6


    def cpcodeData(self, opCode, testData):
        # Version	Opcode	Status code三者长度
        payloadheadlen = 4
        dataLen1 = 0
        for i in testData:
            dataLen1 += testData[i][0]
        dataLen = dataLen1 + payloadheadlen

        payloadData = [self.FRAME_HEAD, self.FRAME_CTR_GET, self.seq, dataLen & 0xff, ((dataLen >>8) & 0xff), self.checkSum, self.PROTO_VER,  opCode & 0xff, ((opCode >>8)& 0xff), self.pStatue]

        #低字节在前
        for i in testData:
            if testData[i][0] == 1:
                payloadData.append(testData[i][1])
            elif testData[i][0] == 2:
                payloadData.append(testData[i][1] & 0xff)
                payloadData.append(((testData[i][1] >> 8) & 0xffff))
            elif testData[i][0] == 4:
                payloadData.append(testData[i][1] & 0xff)
                payloadData.append((testData[i][1] >> 8) & 0xff)
                payloadData.append((testData[i][1] >> 16) & 0xff)
                payloadData.append((testData[i][1] >> 24) & 0xff)
            elif testData[i][0] == 8:
                pass
            else:
                print("数据长度有误，请重新核对！！！")

        lenthData = self.headerlen +  dataLen#固定长度6   payload长度frame_len
        msg_pack = struct.pack("B"*lenthData, *payloadData)

        self.checkSum = opCodeClass().proto_calc_checksum(msg_pack, msg_pack.__len__())
        # print(checksum)
        payloadData[5] = self.checkSum
        msg_pack = struct.pack("B" * lenthData, *payloadData)
        # print(msg_pack)

        print("send -->",str(binascii.b2a_hex(msg_pack))[2:-1].upper())
        return msg_pack

    def proto_calc_checksum(self,ary, len):
        sum = 0
        cnt = 0
        while cnt < len:
            sum = sum + ary[cnt]
            cnt = cnt + 1

        return (0xff - (sum % 256))



    def sendAndReceiveData(self, opCode, testData, responseData):

        ser = serial.Serial(serialCom,115200,timeout=10)
        senddata = opCodeClass().cpcodeData(opCode, testData)
        print(senddata)
        ser.write(senddata)

        count = ser.inWaiting()

        if responseData == {}:
            #header长度6 + payload长度4
            reciveDatalen = 10

        else:
            # header长度6 + payload长度4 + data长度
            dataLen1 = 0
            for i in responseData:
                dataLen1 += responseData[i][0]

            reciveDatalen = 10 + dataLen1

        data = ser.read(reciveDatalen)
        print("receive <--",str(binascii.b2a_hex(data))[2:-1].upper())
        reData = str(binascii.b2a_hex(data))[2:-1].upper()

        return  reData

    def resultData(self, opCode, responseData):
        # Version	Opcode	Status code三者长度
        payloadheadlen = 4
        dataLen1 = 0

        if responseData == {}:
            dataLen = 0x04

            payloadData = [self.FRAME_HEAD, self.FRAME_CTR_ACK, self.seq, dataLen & 0xff, ((dataLen >>8) & 0xff), self.checkSum,
                           self.PROTO_VER, opCode & 0xff, ((opCode >>8)& 0xff), self.pStatue]

            lenthData = self.headerlen +  payloadheadlen#固定长度6   payload长度frame_len
            self.resultDataVal = struct.pack("B"*lenthData, *payloadData)

            self.checkSum = opCodeClass().proto_calc_checksum(self.resultDataVal, self.resultDataVal.__len__())
            # print(self.checkSum)
            payloadData[5] = self.checkSum
            self.resultDataVal = struct.pack("B" * lenthData, *payloadData)

        else:
            for i in responseData:
                dataLen1 += responseData[i][0]
            dataLen = dataLen1 + payloadheadlen

            payloadData = [self.FRAME_HEAD, self.FRAME_CTR_ACK, self.seq, dataLen & 0xff, ((dataLen >>8) & 0xff), self.checkSum,
                           self.PROTO_VER, opCode & 0xff, ((opCode >>8)& 0xff), self.pStatue]

            # 低字节在前
            for i in responseData:
                if responseData[i][0] == 1:
                    payloadData.append(responseData[i][1])
                elif responseData[i][0] == 2:
                    payloadData.append(responseData[i][1] & 0xff)
                    payloadData.append(((responseData[i][1] >>8)& 0xffff))
                elif responseData[i][0] == 4:
                    payloadData.append(responseData[i][1] & 0xff)
                    payloadData.append((responseData[i][1] >> 8)& 0xff)
                    payloadData.append((responseData[i][1] >> 16)& 0xff)
                    payloadData.append((responseData[i][1] >> 24)& 0xff)

                elif responseData[i][0] == 8:
                    pass
                else:
                    print("数据长度有误，请重新核对！！！")

            lenthData = self.headerlen + dataLen  # 固定长度6   payload长度frame_len
            self.resultDataVal = struct.pack("B" * lenthData, *payloadData)

            self.checkSum = opCodeClass().proto_calc_checksum(self.resultDataVal, self.resultDataVal.__len__())
            # print(checksum)
            payloadData[5] = self.checkSum
            self.resultDataVal = struct.pack("B" * lenthData, *payloadData)

        print("resultDataVal -->",str(binascii.b2a_hex(self.resultDataVal))[2:-1].upper())
        self.resultDataVal = str(binascii.b2a_hex(self.resultDataVal))[2:-1].upper()
        return self.resultDataVal

    def resultDataErr(self, opCode, responseData):
        # Version	Opcode	Status code三者长度
        self.pStatue = 0x01
        self.FRAME_CTR_ACK = 0x52
        payloadheadlen = 4
        dataLen1 = 0

        if responseData == {}:
            dataLen = 0x04
            payloadData = [self.FRAME_HEAD, self.FRAME_CTR_ACK, self.seq, dataLen & 0xff, ((dataLen >>8) & 0xff), self.checkSum,
                           self.PROTO_VER, opCode % 256, opCode // 256, self.pStatue]

            lenthData = self.headerlen +  payloadheadlen#固定长度6   payload长度frame_len
            self.resultDataVal = struct.pack("B"*lenthData, *payloadData)

            self.checkSum = opCodeClass().proto_calc_checksum(self.resultDataVal, self.resultDataVal.__len__())
            # print(self.checkSum)
            payloadData[5] = self.checkSum
            self.resultDataVal = struct.pack("B" * lenthData, *payloadData)

        else:
            for i in responseData:
                dataLen1 += responseData[i][0]
            dataLen = dataLen1 + payloadheadlen

            payloadData = [self.FRAME_HEAD, self.FRAME_CTR_ACK, self.seq, dataLen % 256, dataLen // 256, self.checkSum,
                           self.PROTO_VER, opCode & 0xff, ((opCode >>8)& 0xff), self.pStatue]

            # 低字节在前
            for i in responseData:
                if responseData[i][0] == 1:
                    payloadData.append(responseData[i][1])
                elif responseData[i][0] == 2:
                    payloadData.append(responseData[i][1] & 0xff)
                    payloadData.append(((responseData[i][1] >> 8) & 0xffff))
                elif responseData[i][0] == 4:
                    payloadData.append(responseData[i][1] & 0xff)
                    payloadData.append((responseData[i][1] >> 8) & 0xff)
                    payloadData.append((responseData[i][1] >> 16) & 0xff)
                    payloadData.append((responseData[i][1] >> 24) & 0xff)
                elif responseData[i][0] == 8:
                    pass
                else:
                    print("数据长度有误，请重新核对！！！")

            lenthData = self.headerlen + dataLen  # 固定长度6   payload长度frame_len
            self.resultDataVal = struct.pack("B" * lenthData, *payloadData)

            self.checkSum = opCodeClass().proto_calc_checksum(self.resultDataVal, self.resultDataVal.__len__())
            # print(checksum)
            payloadData[5] = self.checkSum
            self.resultDataVal = struct.pack("B" * lenthData, *payloadData)

        print("resultDataVal -->",str(binascii.b2a_hex(self.resultDataVal))[2:-1].upper())
        self.resultDataVal = str(binascii.b2a_hex(self.resultDataVal))[2:-1].upper()
        return self.resultDataVal

    def rebootMcu(self):
        opCode = 0xD101
        testData = {"name1": [1, 0]}
        responseData = {}
        opCodeClass().sendAndReceiveData(opCode, testData, responseData)


    def allModeData(self):
        # 获取ini数据
        testDevice = "P583S"
        con = configparser.ConfigParser()
        con.read(setting.TEST_CONFIG_NEXT, encoding='utf-8')

        mode = con.get(testDevice, "mode")
        recipeId = con.get(testDevice, "recipeId")
        timeMin = con.get(testDevice, "timeMin")
        timeMax = con.get(testDevice, "timeMax")
        tempHahMin = con.get(testDevice, "tempHahMin")
        tempHahMax = con.get(testDevice, "tempHahMax")
        tempDegMin = con.get(testDevice, "tempDegMin")
        tempDegMax = con.get(testDevice, "tempDegMax")
        self.newmode = (mode.split(","))
        self.newrecipeId = (recipeId.split(","))
        self.newtimeMin = (timeMin.split(","))
        self.newtimeMax = (timeMax.split(","))
        self.newtempHahMin = (tempHahMin.split(","))
        self.newtempHahMax = (tempHahMax.split(","))
        self.newtempDegMin = (tempDegMin.split(","))
        self.newtempDegMax = (tempDegMax.split(","))

        # 获取ini数据
        allIniModeData = []
        for iMode in self.newmode:
            dictData = {}
            dictData["mode"] = iMode
            iModeIndex = self.newmode.index(iMode)
            # print(iMode,iModeIndex)
            dictData["recipeId"] = int(self.newrecipeId[iModeIndex])
            dictData["timeMin"] = int(self.newtimeMin[iModeIndex])
            dictData["timeMax"] = int(self.newtimeMax[iModeIndex])
            dictData["tempHahMin"] = int(self.newtempHahMin[iModeIndex])
            dictData["tempHahMax"] = int(self.newtempHahMax[iModeIndex])
            dictData["tempDegMin"] = int(self.newtempDegMin[iModeIndex])
            dictData["tempDegMax"] = int(self.newtempDegMax[iModeIndex])
            allIniModeData.append(dictData)

        return  allIniModeData

if __name__ == "__main__":
    # payload中数据data,namex名称随意，按协议格式输入后面值即可[字节长度,测试值]
    opCode = 0xA405

    testData = {"name1": [1, 17],
                "name2": [1, 1],
                "name3": [1, 1],
                "name4": [4, 0],
                "name5": [2, 205],
                "name6": [4, 60000000],
                "name7": [4, 0],
                "name8": [2, 0]}

    #应答数据,无应答数据，为空字典，有数据与testData格式一致。
    responseData = {
    }

    opCodeClass().sendAndReceiveData(opCode, testData, responseData)
    opCodeClass().resultData(opCode,responseData)
