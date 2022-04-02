# -*- coding: utf-8 -*-

import _thread
import base64
import hashlib
import json
import struct
import time

import requests
import serial
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5     # 生成对象
from lib.logGet import *
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()

# AES 密钥
G_AES_KEY = struct.pack('BBBBBBBBBBBBBBBB', 0x6c, 0x6c, 0x77, 0x61, 0x6e, 0x74, 0x61, 0x65, 0x73, 0x6b, 0x65, 0x79,
                        0x31, 0x2e, 0x30, 0x31)
G_AES_IV = struct.pack('BBBBBBBBBBBBBBBB', 0x6c, 0x6c, 0x77, 0x61, 0x6e, 0x74, 0x61, 0x65, 0x73, 0x69, 0x76, 0x76, 0x31,
                       0x2e, 0x30, 0x31)

# 定义协议字段
FRAME_HEAD = 0xA5
FRAME_END = 0x5A

# 控制码定义
FRAME_CTR_GET = 0x22
FRAME_CTR_ACK = 0x12

# 协议版本
PROTO_VER = 0x01

# OP_CODE 定义
OP_KEY_EXCHANGE = 0x8000
OP_GET_DEVICE_INFO = 0x8010
OP_GET_WIFI_LIST = 0x8011
OP_SET_CONFIG_INFO = 0x8012
OP_CONFIG_RESULT = 0x8013
OP_CONFIG_LOG = 0x8014
OP_CONFIG_ERROR = 0x8015
OP_GET_CACHE_LOG = 0x8017

# 应答
FRAME_RECEIVE_HEAD = 0
FRAME_RECEIVE_CTRL = 1
FRAME_RECEIVE_SEQ = 2
FRAME_RECEIVE_LEN_L = 3
FRAME_RECEIVE_LEN_H = 4
FRAME_RECEIVE_SUM = 5
FRAME_RECEIVE_PAYLOAD = 6

rcv_status = FRAME_RECEIVE_HEAD
g_frame_ctr = 0
g_frame_seq = 0
g_frame_payload_len = 0
g_frame_pos = 0
g_frame_payload = b''
g_opcode = 0

g_pubkey = None
g_privkey = None

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


# 串口打开及发送
class serial_com():
    def __init__(self, com, bsp):
        self.serial = None
        try:
            self.serial = serial.Serial(com, bsp, timeout=10)
            if self.serial.isOpen():
                logger.info(">> " + com + " 蓝牙透传dongle打开成功")
            else:
                logger.info(">> " + com + " 蓝牙透传dongle打开失败")
        except Exception as e:
            raise e

    def data_send(self, send_data):
        if self.serial is None:
            return
        else:
            try:
                print("send_data", send_data)
                self.serial.write(send_data)

            except Exception as e:
                logger.info(str(e))


# 加密解密
class AES_CBC:

    def add_to_16(self, value):
        while len(value) % 16 != 0:     # 如果text不足16位的倍数就用空格补足为16位
            value += '\0'
        return str.encode(value)  # 返回bytes

    # 加密方法
    def encrypt_oracle(self, text):
        # 初始化加密器
        aes = AES.new(G_AES_KEY, AES.MODE_CBC, G_AES_IV)
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7
        encrypt_aes = aes.encrypt(str.encode(pad2(text)))
        return encrypt_aes

    # 解密方法
    def decrypt_oralce(self, text):
        aes = AES.new(G_AES_KEY, AES.MODE_CBC, G_AES_IV)
        plain_text = aes.decrypt(text)
        logger.info(str(plain_text, 'utf-8'))
        return unpad(plain_text)


# 秘钥协商应答处理，更新AES秘钥
def proto_key_exchange_respone_handle(data_payload):
    global g_privkey
    global G_AES_KEY
    global G_AES_IV
    global ase_key

    aes = AES_CBC()
    decrypt_data = aes.decrypt_oralce(data_payload)
    hjson = json.loads(decrypt_data.decode('utf-8'))
    aes_key_base64 = hjson['key']
    iv_key_base64 = hjson['iv']
    logger.info('>> aes_key_base64 = %s' % aes_key_base64)
    logger.info('>> iv_key_base64 = %s' % iv_key_base64)

    ase_key_crypto = base64.decodebytes(aes_key_base64.encode())
    iv_key_crypto = base64.decodebytes(iv_key_base64.encode())

    cipher = PKCS1_v1_5.new(g_privkey)
    ase_key = cipher.decrypt(ase_key_crypto, 'xyz')
    iv_key = cipher.decrypt(iv_key_crypto, 'xyz')

    G_AES_KEY = ase_key
    G_AES_IV = iv_key

    if len(ase_key) != 16:
        logger.warning('G_AES_KEY长度不匹配=================================================' + str(len(ase_key)))

    G_AES_KEY = ase_key
    G_AES_IV = iv_key

    # G_AES_KEY_HEX = []
    # for arr in G_AES_KEY:
    #     arr = hex(arr)
    #     G_AES_KEY_HEX.append(arr)
    #
    # G_AES_IV_HEX = []
    # for arr in G_AES_IV:
    #     arr = hex(arr)
    #     G_AES_IV_HEX.append(arr)
    #
    # logger.info(">> G_AES_KEY_HEX: " + str(G_AES_KEY_HEX))
    # logger.info(">> G_AES_IV_HEX: " + str(G_AES_IV_HEX))


# hex打印
def print_hex_ary(ary):
    cnt = 0
    len = ary.__len__()
    while cnt < len:
        # logger.info('%02x' % ary[cnt], )
        print('%02x' % ary[cnt],end=' ')
        cnt = cnt + 1


# 计算校验和
def proto_calc_checksum(ary, len):
    sum = 0
    cnt = 0
    while cnt < len:
        sum = sum + ary[cnt]
        cnt = cnt + 1
    return (0xff - (sum % 256))


# 通用协议大纲封装
def proto_base_pack(op_code):
    frame_len = 4
    seq = 0x01
    checksum = 0
    # Header格式：6 bytes 包括1byte:起始符  1byte: 控制标志  1byte: 数据包流水号 2bytes:payload长度  1byte: 校验和
    # payload格式： 0-65535 bytes  包括1byte: 业务版本  2bytes:opcode   1byte:状态码  0-65531bytes: data
    # eg：A5 22 01 04 00 A2 01 10 80 00   0x8010
    msg_pack = struct.pack("BBBBBBBBBB", FRAME_HEAD, FRAME_CTR_GET, seq, frame_len % 256, (frame_len // 256), checksum,
                           PROTO_VER, op_code % 256, op_code // 256, 0)
    checksum = proto_calc_checksum(msg_pack, msg_pack.__len__())
    msg_pack = struct.pack("BBBBBBBBBB", FRAME_HEAD, FRAME_CTR_GET, seq, frame_len % 256, (frame_len // 256), checksum,
                           PROTO_VER, op_code % 256, op_code // 256, 0)
    print_hex_ary(msg_pack, type(msg_pack))
    return msg_pack


# pyaload数据封装
def proto_payload_pack(op_code, payload):
    frame_len = 4 + payload.__len__()
    seq = 0x01
    checksum = 0
    msg_pack = struct.pack("BBBBBBBBBB", FRAME_HEAD, FRAME_CTR_GET, seq, frame_len % 256, (frame_len // 256),
                           checksum, PROTO_VER, op_code % 256, op_code // 256, 0) + payload
    checksum = proto_calc_checksum(msg_pack, msg_pack.__len__())
    msg_pack = struct.pack("BBBBBBBBBB", FRAME_HEAD, FRAME_CTR_GET, seq, frame_len % 256, (frame_len // 256),
                           checksum, PROTO_VER, op_code % 256, op_code // 256, 0) + payload
    return msg_pack


# http请求：Vesync账号密码校验
def user_login():
    # email = "stoneshi@test.com"
    # password = "shican"
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    password_md5 = m.hexdigest()
    millis = int(round(time.time() * 1000))
    traceId = str(millis)

    global g_token
    global g_accountID

    try:
        url = server1 + "/cloud/v1/user/login"
        data = "{\"userType\": \"1\",\"phoneOS\": \"iOS12.1.4\",\"acceptLanguage\": \"en\",\"phoneBrand\": \"iPhone 6s\",\"timeZone\": \"Asia\/Shanghai\",\"token\": \"\",\"appVersion\": \"V2.8.0 build2019071215\",\"accountID\": \"\",\"method\": \"login\",\"traceId\": \"" + traceId + "\",\"email\": \"" + email + "\",\"password\":\"" + password_md5 + "\"}"
        res = requests.post(url, json=json.loads(data), verify=False, timeout=10)
        hjson = json.loads(res.text)
        g_token = hjson['result']['token']
        g_accountID = hjson['result']['accountID']
        logger.info(">> Vesync用户信息获取成功")
        # logger.info("token:" + g_token + ",accountID:" + g_accountID + "\r")
    except Exception as e:
        logger.error("账号密码校验失败，请检查后重试。")
        logger.error("!!! " + str(e))
        return False

# http请求：云端获取配网信息
def get_configkey():
    millis = int(round(time.time() * 1000))
    traceId = str(millis)

    try:
        url = server1 + "/cloud/v1/deviceManaged/configInfo"
        data = "{\"phoneOS\": \"iOS 14.5\",\"acceptLanguage\": \"en\",\"region\": \"us-newVersion\",\"phoneBrand\": \"iPhone 6s\",\"timeZone\": \"Asia\/Shanghai\",\"appVersion\": \"VeSycn 3.1.111 build15\",\"method\": \"configInfo\",\"traceId\": \"" + traceId + "\",\"token\": \"" + g_token + "\",\"accountID\":\"" + g_accountID + "\",\"configModule\":\"" + configModule + "\"}"
        res = requests.post(url, json=json.loads(data), verify=False, timeout=10)
        hjson = json.loads(res.text)
        global configkey
        global serverDN
        global serverIP
        global pid
        configkey = hjson['result']['configkey']
        serverDN = hjson['result']['serverUrl']
        serverIP = hjson['result']['ip']
        pid = hjson['result']['pid']
        logger.info("HTTP查询：获取配网信息")
        logger.info(res.text + "\r")
        # return configkey

    except Exception as e:
        logger.error("云端获取配网信息失败，请重试。")
        logger.error("!!! " + str(e))
        time.sleep(5)
        get_configkey()  # 重试


# http请求：获取设备列表
def get_device_list():
    millis = int(round(time.time() * 1000))
    traceId = millis

    try:
        url = server1 + "/cloud/v1/deviceManaged/devices"

        data = {'phoneOS': 'iOS 14.5', 'acceptLanguage': 'en', 'region': 'us-newVersion', 'phoneBrand': 'iPhone 6s',
                'timeZone': 'Asia/Shanghai',
                'appVersion': 'VeSycn 3.1.111 build15', 'method': 'devices', 'traceId': traceId, 'token': g_token,
                'accountID': g_accountID,
                'pageSize': 100, 'pageNum': 10}

        res = requests.post(url, json=data, verify=False, timeout=20)
        # print(res.text)
        if g_cid in res.text:
            logger.info("HTTP查询：设备配网成功")
            hjson = json.loads(res.text)['result']['list']  # 设备列表
            i = 0
            while i < len(hjson):
                if hjson[i]['cid'] == g_cid:
                    if hjson[i]['connectionStatus'] == "online":
                        logger.info(("HTTP查询：设备当前在线"))
                    else:
                        logger.info(("HTTP查询：设备当前离线，retry"))
                        time.sleep(10)
                        get_device_list()  # 重试
                i = i + 1
        else:
            logger.warning("HTTP查询：设备不存在，retry")
            i = 1
            while i <= 10:
                time.sleep(10)
                res = requests.post(url, json=data, verify=False, timeout=20)
                if g_cid in res.text:
                    logger.warning("HTTP查询：设备配网成功")
                    break
                else:
                    logger.warning("HTTP查询：设备不存在，retry:" + str(i))
                i = i + 1

    except Exception as e:
        logger.error("查询设备配网失败")
        logger.error("!!! " + str(e))
        time.sleep(5)
        get_device_list()  # 重试


# http请求：删除设备重新触发配网
def del_device():
    millis = int(round(time.time() * 1000))
    traceId = millis
    try:
        url = server1 + "/cloud/v1/deviceManaged/deleteDevice"

        data = {'phoneOS': 'iOS 14.5', 'acceptLanguage': 'en', 'region': 'us-newVersion', 'phoneBrand': 'iPhone 6s',
                'timeZone': 'Asia/Shanghai',
                'appVersion': 'VeSycn 3.1.111 build15', 'method': 'deleteDevice', 'traceId': traceId, 'token': g_token,
                'accountID': g_accountID,
                'configModule': configModule, 'cid': g_cid}

        res = requests.post(url, json=data, verify=False, timeout=10)
        hjson = json.loads(res.text)

        ret = hjson['code']
        if ret == 0:
            logger.info("HTTP下发：设备删除成功")
        else:
            logger.warning("HTTP下发：设备删除失败，retry")
            logger.warning(res.text)
            time.sleep(5)
            res = requests.post(url, json=data, verify=False, timeout=10)
            logger.warning(res.text)

    except Exception as e:
        logger.error("HTTP下发：设备删除失败")
        logger.error("!!! " + str(e))
        time.sleep(5)
        res = requests.post(url, json=data, verify=False, timeout=10)
        logger.error("!!! " + str(e))


# tcp请求，删除设备重新触发配网
# def send_socket():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(5)  # 设置连接超时
#         s.connect((ipaddr, 55555))
#         cmd = "{\"traceId\":\"1585045200000\",\"method\":\"bypassV2\",\"cid\":\"XXXXXXXX\",\"payload\":{\"method\":\"resetDevice\",\"data\":{\"type\":\"delDevice\"}}}"  # 对应命令
#         s.send(cmd.encode())
#         logger.info("TCP 发送：设备删除成功")
#         s.close()
#     except Exception as e:
#         logger.error("TCP 发送：设备删除失败 " + str(e))
#         time.sleep(5)
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             s.settimeout(5)  # 设置连接超时
#             s.connect((ipaddr, 55555))
#             cmd = "{\"traceId\":\"1585045200000\",\"method\":\"bypassV2\",\"cid\":\"XXXXXXXX\",\"payload\":{\"method\":\"resetDevice\",\"data\":{\"type\":\"delDevice\"}}}"  # 对应命令
#             s.send(cmd.encode())
#             logger.info("TCP 发送：设备删除成功")
#             s.close()
#         except Exception as e:
#             logger.error("TCP 发送：设备删除失败 " + str(e))
#

# 配网密钥协商
def config_key_exchange():
    # 生成密钥
    global g_pubkey
    global g_privkey
    global G_AES_KEY
    global G_AES_IV

    logger.info("蓝牙发送：配网密钥协商(0x8000)")

    # 秘钥协商使用初始化秘钥
    G_AES_KEY = struct.pack('BBBBBBBBBBBBBBBB', 0x6c, 0x6c, 0x77, 0x61, 0x6e, 0x74, 0x61, 0x65, 0x73, 0x6b, 0x65, 0x79,
                            0x31, 0x2e, 0x30, 0x31)
    G_AES_IV = struct.pack('BBBBBBBBBBBBBBBB', 0x6c, 0x6c, 0x77, 0x61, 0x6e, 0x74, 0x61, 0x65, 0x73, 0x69, 0x76, 0x76,
                           0x31, 0x2e, 0x30, 0x31)
    # ========RSA加密处理==============
    private = RSA.generate(1024)    # 指定长度1024
    public = private.publickey()
    private_key = private.exportKey().decode()  # 生成私钥
    public_key = public.exportKey().decode()    # 生成公钥
    g_pubkey = public_key
    g_privkey = RSA.importKey(private_key)  # 导入读取到的私钥
    json_data = {'key': g_pubkey}
    print(json_data)
    aes = AES_CBC()
    encrypt_data = aes.encrypt_oracle(json.dumps(json_data))
    msg_pack = proto_payload_pack(OP_KEY_EXCHANGE, encrypt_data)

    logger.info("【=========TX数据=========>%s" % msg_pack)
    return msg_pack


# 蓝牙：查询缓存日志
def get_cache_log():
    msg_pack = proto_base_pack(OP_GET_CACHE_LOG)
    logger.info("蓝牙发送：查询缓存日志(0x8017)")
    print_hex_ary(msg_pack)
    return msg_pack


# 蓝牙：查询设备信息
def get_device_info():
    msg_pack = proto_base_pack(OP_GET_DEVICE_INFO)
    logger.info("蓝牙发送：查询设备信息(0x8010)")

    print_hex_ary(msg_pack)
    return msg_pack


# 蓝牙：查询wifi列表
def get_wifi_list(page, needScan):
    json_data = {'page': page, 'needScan': needScan}
    aes = AES_CBC()
    encrypt_data = aes.encrypt_oracle(json.dumps(json_data))
    msg_pack = proto_payload_pack(OP_GET_WIFI_LIST, encrypt_data)
    if needScan == 0:
        logger.info("蓝牙发送：查询缓存列表(0x8011)")
    elif needScan == 1:
        logger.info("蓝牙发送：查询实时列表(0x8011)")
    else:
        pass

    print_hex_ary(msg_pack)
    # logger.info(msg_pack)
    return msg_pack         # 返回封装好的数据


# 蓝牙：发送配网信息
def set_netconfig_info():
    json_data = {'serverDN': serverDN, 'configKey': configkey, 'serverIP': serverIP, 'tcpDebugPort': 'on',
                 'wifiSSID': wifiSSID, 'wifiPassword': wifiPassword, 'pid': pid, 'accountID': g_accountID,
                 "needReset": 0}

    print(json_data)
    aes = AES_CBC()
    encrypt_data = aes.encrypt_oracle(json.dumps(json_data))
    msg_pack = proto_payload_pack(OP_SET_CONFIG_INFO, encrypt_data)
    logger.info("蓝牙发送：下发配网信息(0x8012)")
    # logger.info(">> " + str(json_data))
    print_hex_ary(msg_pack)
    return msg_pack


# 封装应答包
def proto_ack_pack(seq, status_code):
    global g_opcode
    frame_len = 4
    checksum = 0
    msg_pack = struct.pack("BBBBBBBBBB", FRAME_HEAD, FRAME_CTR_ACK, seq, frame_len % 256, (frame_len // 256),
                           checksum, PROTO_VER, g_opcode % 256, g_opcode // 256, status_code)
    checksum = proto_calc_checksum(msg_pack, msg_pack.__len__())
    msg_pack = struct.pack("BBBBBBBBBB", FRAME_HEAD, FRAME_CTR_ACK, seq, frame_len % 256, (frame_len // 256),
                           checksum, PROTO_VER, g_opcode % 256, g_opcode // 256, status_code)
    return msg_pack


def proto_decode_handle(data_byte):
    global rcv_status
    global g_frame_ctr
    global g_frame_seq
    global g_frame_payload_len
    global g_frame_pos
    global g_frame_payload
    ret = 1
    if rcv_status == FRAME_RECEIVE_HEAD:
        if data_byte == FRAME_HEAD:
            rcv_status = FRAME_RECEIVE_CTRL
    elif rcv_status == FRAME_RECEIVE_CTRL:
        g_frame_ctr = data_byte
        rcv_status = FRAME_RECEIVE_SEQ
    elif rcv_status == FRAME_RECEIVE_SEQ:
        g_frame_seq = data_byte
        rcv_status = FRAME_RECEIVE_LEN_L
    elif rcv_status == FRAME_RECEIVE_LEN_L:
        g_frame_payload_len = data_byte
        rcv_status = FRAME_RECEIVE_LEN_H
    elif rcv_status == FRAME_RECEIVE_LEN_H:
        g_frame_payload_len = g_frame_payload_len + data_byte * 256
        rcv_status = FRAME_RECEIVE_SUM
    elif rcv_status == FRAME_RECEIVE_SUM:
        if g_frame_payload_len > 0:
            rcv_status = FRAME_RECEIVE_PAYLOAD
            g_frame_pos = 0
            g_frame_payload = b''
        else:
            rcv_status = FRAME_RECEIVE_HEAD
            ret = 0
    elif rcv_status == FRAME_RECEIVE_PAYLOAD:
        g_frame_payload = g_frame_payload + struct.pack('B', data_byte)
        g_frame_pos = g_frame_pos + 1
        if g_frame_pos >= g_frame_payload_len:
            ret = 0
            rcv_status = FRAME_RECEIVE_HEAD

    return ret


# 获取数据payload
def proto_get_data_payload(frame_payload):
    if frame_payload.__len__() < 5:
        return None
    cnt = 0
    dat = b''
    while cnt < frame_payload.__len__() - 4:
        dat = dat + struct.pack('B', frame_payload[4 + cnt])
        cnt = cnt + 1
    return dat


# 协议应答
def proto_ack_handle(serial):
    global g_frame_seq
    msg = proto_ack_pack(g_frame_seq, 0)
    # print_hex_ary(msg)
    serial.write(msg)


def serial_relay_run(threadName):
    serial_data_handle_loop()

# 串口接收数据处理
def serial_data_handle_loop():
    global serial
    global g_opcode

    if serial is None:
        return
    while True:
        dat = serial.serial.read_all()
        if dat != b'':
            cnt = 0
            # print(str(dat, encoding="utf-8"))
            # print_hex_ary(dat)

            while cnt < dat.__len__():
                if proto_decode_handle(dat[cnt]) == 0:
                    # logger.info('proto decode ok')
                    g_opcode = g_frame_payload[1]
                    g_opcode = g_frame_payload[2] * 256 + g_opcode

                    if g_opcode == OP_KEY_EXCHANGE:  # 秘钥协商返回 0x8000
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_key_exchange_respone_handle(data_pl)
                    elif OP_GET_CACHE_LOG == g_opcode:  # 获取缓存日志 0x8017
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                    elif OP_GET_DEVICE_INFO == g_opcode:  # 获取设备信息 0x8010
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                    elif OP_GET_WIFI_LIST == g_opcode:  # 获取WIFI列表 0x8011
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                    elif OP_SET_CONFIG_INFO == g_opcode:  # 下发配网应答 0x8012
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                    elif OP_CONFIG_RESULT == g_opcode:  # 获取配网结果日志 0x8013
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                    elif OP_CONFIG_LOG == g_opcode:  # 获取配网过程日志 0x8014
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                    elif OP_CONFIG_ERROR == g_opcode:  # 获取配网失败日志 0x8015
                        data_pl = proto_get_data_payload(g_frame_payload)
                        proto_device_log_handle(data_pl)
                        # logger.info(">> 配网失败,重新配网.")
                        # time.sleep(120)
                        # serial.data_send(set_netconfig_info())  # 发送配网信息

                    # logger.info('g_frame_ctr = %x' % g_frame_ctr)
                    # logger.info('g_opcode = %x' % g_opcode)
                    if g_frame_ctr == FRAME_CTR_GET:
                        logger.info(">> receive response.")
                        proto_ack_handle(serial.serial)  # 回复命令
                    break
                cnt = cnt + 1
        # time.sleep(0.1)


# 配网日志处理解密打印
def proto_device_log_handle(data_payload):
    try:
        aes = AES_CBC()
        decrypt_data = aes.decrypt_oralce(data_payload)
        logger.info('>> ' + str(hex(g_opcode)) + ": " + str(decrypt_data)[2:-1])
    except Exception as e:
        pass

def push_button(ser2, t):
    #1通道继电器
    COMMAND_PORT_ON_1 = [51, 1, 18, 0, 0, 0, 1, 71]
    COMMAND_PORT_OFF_1 = [51, 1, 17, 0, 0, 0, 1, 70]

    logger.info("按电源键5s,设备开始进入配网")
    ser2.data_send(COMMAND_PORT_ON_1)
    time.sleep(t)
    ser2.data_send(COMMAND_PORT_OFF_1)



if __name__ == '__main__':

    '''
    @1******测试前，需要知道被测设备cid和onfigModule
    @2******ESP32开发板(烧录配网主机工具程序),把ESP32_DEVKITC_V4板子靠近待测设备,
    按一下板子上的boot按键,就会开始配对绑定,配对成功后即可以进行数据收发
    '''


    #净化器Core300s芯邦us
    g_cid = 'fwtest-ddy6oRXm_ebo97lU-abxQGEcv'
    configModule = 'VS_WFON_AFR_CAF-P583S-KEU_ONL_EU'

    # 配网配置
    server1 = "https://test-online.vesync.com"
    email = "elevenliu@vesync.com.cn"
    password = "123456"
    wifiSSID = "Eleven_VvV"
    wifiPassword = "12345678"
    # ipaddr = "192.168.0.178"  # 设备ip，通过tcp删除设备

    ser2 = serial_com("COM13", 9600)  # 继电器com口,波特率固定为9600
    serial = serial_com("COM16", 115200)  # 蓝牙透传工具com口,波特率固定115200

    _thread.start_new_thread(serial_relay_run, ("serial_thread",))  # 蓝牙监听消息回复
    logger.info(">> 蓝牙监听：固件上报日志回复")
    user_login()  # 用户登录获取用户信息
    i = 1
    while i < 20000:  # 配网次数
        logger.info("==========Round=========" + str(i))

        #按键5s以上触发配网
        push_button(ser2, 7)
        time.sleep(3)

        get_configkey()  # 获取配网configkey
        serial.data_send(config_key_exchange())  # 密钥协商
        time.sleep(4)
        while len(G_AES_KEY) != 16:  # 协商解密的aeskey不为16位重新协商
            serial.data_send(config_key_exchange())  # 密钥协商
            time.sleep(4)
        serial.data_send(get_cache_log())  # 查询缓存日志
        time.sleep(2)
        serial.data_send(get_device_info())  # 获取设备信息
        time.sleep(2)
        # =====循环获取WiFi列表=====
        print("=====循环获取WiFi列表=====")
        serial.data_send(get_wifi_list(1, 0))   # 0查缓存 1查实时
        time.sleep(10)
        # 发送配网信息
        serial.data_send(set_netconfig_info())
        time.sleep(10)
        get_device_list()  # 查询设备列表判断是否配网成功,失败循环
        time.sleep(1)
        del_device()  # 通过http删除设备
        # # # send_socket()  # 通过tcp删除设备
        time.sleep(10)
        i = i + 1


