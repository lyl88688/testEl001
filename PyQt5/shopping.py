#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import oauth2 as oauth

import json

import requests

import time, random

import base64

import rsa.common

from Crypto.PublicKey import RSA





url1 = "https://testonline-store.vesync.com"

# token = "SKQDheh9gdgfpx4sBVe-o0E_ej7R-jC08cPJklcyM2glmw=="  #predeploy

token = "rpJH4LBhczg-N708Xw01CIVR5YgIqs2V1TM2nimf6HBshOCmxw=="



id = "1165800"

# headerx = {"Content-Type": "application/json"}





def unix_time():

    millis = str(round(time.time() * 1000))  # 时间戳

    unix_time = "APPC2F5" + millis + "-00057"

    return unix_time





def devices_info():

    """

    设备信息

    :return:

    """

    info = {"context": {"traceId": unix_time(),

                        "method": "addCartProduct",

                        "reqTimestamp": int(round(time.time() * 1000)),

                        "timeZone": "Asia/Shanghai",

                        "clientInfo": "PDEM10",

                        "terminalId": "28079309332e7364c8c2fee6b176c2f53",

                        "clientVersion": "VeSync 3.1.0_210102_build1",

                        "token": token,

                        "accountID": id,

                        "osInfo": "Android 10",

                        "clientType": "vesyncApp",

                        "acceptLanguage": "en",

                        "debugMode": False},

            "data": ""}

    return info





class RsaEncrypt:

    def rsa_encrypt_bytes(self, pub_key, bytes_str):

        if not isinstance(bytes_str, bytes):

            return None

        pubkey = rsa.PublicKey(pub_key.n, pub_key.e)

        key_length = rsa.common.byte_size(pub_key.n)

        max_msg_length = key_length - 11

        count = len(bytes_str) // max_msg_length

        if len(bytes_str) % max_msg_length > 0:

            count = count + 1

        cry_bytes = b''

        # rsa加密要以max_msg_length分组, 每组分别加密(加密的数据长度为key_length, 解密时每key_length长度解密然后相加)

        for i in range(count):

            start = max_msg_length * i

            size = max_msg_length

            content = bytes_str[start: start + size]

            # rsa 分组 加密

            crypto = rsa.encrypt(content, pubkey)

            cry_bytes = cry_bytes + crypto

        return cry_bytes

    # rsa 解密, bytes_string是rsa_encrypt_hex, rsa_encrypt_bytes的返回值



    def rsa_decrypt(self, pri_key, bytes_string):

        """

        rsa解密函数

        :param pri_key:

        :param bytes_string:

        :return:

        """

        # 导入rsa库

        pri_key = rsa.PrivateKey(pri_key.n, pri_key.e, pri_key.d, pri_key.p, pri_key.q)

        key_length = rsa.common.byte_size(pri_key.n)

        if len(bytes_string) % key_length != 0:

            # 如果数据长度不是key_length的整数倍, 则数据是无效的

            return None

        count = len(bytes_string) // key_length

        d_cty_bytes = b''

        # 分组解密

        for i in range(count):

            start = key_length * i

            size = key_length

            content = bytes_string[start: start + size]

            # rsa 分组 解密

            d_crypto = rsa.decrypt(content, pri_key)

            d_cty_bytes = d_cty_bytes + d_crypto

        return d_cty_bytes



    # rsa 加密, 注意: 这里是传递的是16进制字符串

    def rsa_encrypt_hex(self, pub_key, hex_string):

        return self.rsa_encrypt_bytes(pub_key, bytes.fromhex(hex_string))



    def test_encrypt_decrypt(self):

        """

        rsa 库的测试

        :return:

        """

        # 产生公钥私钥

        (pub, pri) = rsa.newkeys(256)

        # 构建新的公钥私钥

        pub_key = rsa.PublicKey(pri.n, pri.e)

        pri_key = rsa.PrivateKey(pri.n, pri.e, pri.d, pri.p, pri.q)

        message = b'\x00\x00\x00\x00\x01'

        # 加密 message

        crypto = rsa.encrypt(message, pub_key)

        # 解密

        d_crypto = rsa.decrypt(crypto, pri_key)

        print(d_crypto)



    def read_keys_from_pem_file(self):

        # with open(pub_key_file, 'r') as f:

        #     _key = f.read()

        #     _pub_key = RSA.importKey(_key)  # 导入读取到的公钥

        # with open(pri_key_file, 'r') as f:

        #     _key = f.read()

        #     _pri_key = RSA.importKey(_key)  # 导入读取到的私钥

        public_key = """-----BEGIN PUBLIC KEY-----

MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCPs56I7iBzQHMAopeA/M5CjkNTBtnT6J3gX1rVoc40D1vQOz+tiKpx7UWLEgrK0cnFL81sfL+cfr1smn1UGIDmTA5s9Tn+NYwphrmWffGVWLnxixLFgv2kj3Nex+20JYEBbmbO+WtFVxpF9jdREN+BcDEOvWRnMU7REZAwa2V3GwIDAQAB

-----END PUBLIC KEY-----"""

        private_key = """-----BEGIN RSA PRIVATE KEY-----

MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAI+znojuIHNAcwCil4D8zkKOQ1MG2dPoneBfWtWhzjQPW9A7P62IqnHtRYsSCsrRycUvzWx8v5x+vWyafVQYgOZMDmz1Of41jCmGuZZ98ZVYufGLEsWC/aSPc17H7bQlgQFuZs75a0VXGkX2N1EQ34FwMQ69ZGcxTtERkDBrZXcbAgMBAAECgYA2QpJ4DcI/AnTqJnqif9K6GtGdBhc2Br2mPRslU2VzDuGSLO0Mb3A8eGUr7/IXR0Oyqywb7LbFNq371hHAsUfqG+Ig22YEM+eQxyA+u6F5GvOxldC+kEbAflSWuBLsTfSF5JMfI29NmtTJ7T7EGyRFV7+B2FPE3gK3EQ6qiaEREQJBANUsvG2Plr+cKVaGR3/d200Hq62b1Xql4jA2zTMgBNJVvWkoX5kem5I/FEGZsMxuNCLshj7mDLY6DUO9AWMg2x0CQQCskfuzzzyh/Ubb4JHinne6qk03F1hM+rUZMGRYeXjGwbSwInG1WjRZwnYl/a09tuDNWh4GJIER//XF8dnOZs2XAkEAveNtrYJ8XA403HgcdJAhawpsKOdpUCk3xI7sVqAs61eos2VdUr3rAmjiGFVZIaEBHCLoqlqt9Bzd9/sCo1R/GQJAMRZtdJ5UbveuukjM9puBDzX2NN+NHIiMDxg20vvqoQ7kqN2DXsTD82xfUzsvlkh49bDWrYSgulAGx0GeZRnVDQJACOhaGT1YsNrBOJTaUWXoqC+WYdIyfTwF/ZWzFapSYJBgOkVSf7C/EjoXh3tNoT7KaMZvaA1vR1XkJ11jwEoqcw==

-----END RSA PRIVATE KEY-----"""

        _pub_key = RSA.importKey(public_key)  # 导入读取到的公钥

        _pri_key = RSA.importKey(private_key)  # 导入读取到的私钥

        return _pub_key, _pri_key





def ShippingDetail():

    """

    查询订单消息

    :return:

    """

    print("查询订单信息")

    try:

        url = url1 + "/vmall/v1/shipping/addOrderShippingDetail"

        payload = {

            "orderShippingInfos": [

                {

                    "orderNumber": "50433484607",

                    "shippingNumber": "1ZE4F435000002894",

                    "shippingCompanyId": 2,

                    "startLocation": "Bethel,DE"},

                {

                    "orderNumber": "50433484607",

                    "shippingNumber": "787660401905",

                    "shippingCompanyId": 1,

                    "startLocation": "Bethel,DE"

                }

            ]

        }

        data = devices_info()

        data["data"] = payload

        data["context"]["method"] = "addOrderShippingDetail"

        # =======rsa加密========

        num = len(payload["orderShippingInfos"])            # 改了这里

        # print(num)

        a = RsaEncrypt()

        pubKey, priKey = a.read_keys_from_pem_file()

        bts_str = (str(num)).encode()       # 改了这里

        crypto_bytes = a.rsa_encrypt_bytes(pubKey, bts_str)

        cipher_text = base64.b64encode(crypto_bytes)

        # print(cipher_text.decode('utf-8'))

        #print(data)

        # =======rsa加密========

        num = cipher_text.decode('utf-8')       # 改了这里

        headerx = {"Content-Type": "application/json", "OrderShippingInfoListSize": num}  # 新增

        rec = requests.post(url, data=json.dumps(data), headers=headerx)

        print(rec.headers)

        print("\nResult: " + rec.text)

    except Exception as e:

        print("查询订单信息异常： " + str(e))





if __name__ == '__main__':

    ShippingDetail()   # 查询订单消息

