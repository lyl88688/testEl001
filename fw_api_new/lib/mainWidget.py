
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
界面功能
"""


import os,sys
sys.path.append(os.path.dirname(__file__))
from requests.packages import urllib3
# 禁用安全请求警告
urllib3.disable_warnings()
sys.path.append(os.path.dirname(__file__))
import configparser
import ctypes
import hashlib
import inspect
import threading
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from lib.thirdpartui import *

from PyQt5.QtCore import  QEventLoop, QTimer
from lib.commonApi import *
from lib.caseSuite import *
from lib import globalName



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.device = None  # 所有设备列表的参数
        self.device_mac = None
        self.Language = None
        self.third_device = None
        self.row_no = None
        self.excel = None
        self.setupUi(self)
        self.cfg_check()  # 检查配置文件并创建
        self.comboBox.activated[str].connect(self.login)
        self.comboBox_2.activated[str].connect(self.display_device_info)

        self.pushButton.clicked.connect(self.running)  # pushbutton是开始测试按钮
        self.pushButton_4.clicked.connect(self.textclear)

    def flush(self):
        pass

    def genMastClicked(self):
        """Runs the main function."""
        print('Running...')
        loop = QEventLoop()
        QTimer.singleShot(5000, loop.quit)
        loop.exec_()
        print('Done.')

    def select_test_file(self):
        get_filenames_path, ok = QFileDialog.getOpenFileNames(self, "选取多个文件", "./", "All Files (*);;Text Files (*.bin)")
        self.lineEdit_5.setText(str(get_filenames_path[0]))

    def cfg_check(self):
        try:
            con = configparser.ConfigParser()
            con.read(setting.TEST_CONFIG, encoding='utf-8')
            email = con.get('tester', 'email')
            password = con.get('tester', 'password')
            logger.debug("cfg_check: 账号-->%s 请求响应异常--->%s" % (email, password))
            # 导入配置
            self.lineEdit.setText(email)
            self.lineEdit_2.setText(password)

        except Exception as e:
            logger.error(" cfg_check 异常--> %s " % e)

    # 配置文件写值函数
    def cfg_write(self, name, value):
        conf = configparser.ConfigParser()  # 加载配置文件
        logger.debug("cfg_write", setting.TEST_CONFIG)
        conf.read(setting.TEST_CONFIG, encoding='utf-8')
        conf.set('tester', name, value)  # 设置参数
        # 写回配置文件
        conf.write(open(setting.TEST_CONFIG, "w"))

    # 保存控件配置
    def cfg_save(self):
        # 保存配置文件
        try:
            self.cfg_write('email', str(self.lineEdit.text()))
            self.cfg_write('password', str(self.lineEdit_2.text()))
        except Exception as e:
            logger.error(" cfg_save 异常--> %s " % e)

    def textclear(self):
        self.textBrowser.clear()

    def display_device_info(self):
        num = self.comboBox_2.currentIndex()
        globalName.device_cid = self.device[num]['cid']
        #设备Module
        globalName.device_configModule = self.device[num]['configModule']

        globalName.device_uuid = self.device[num]['uuid']
        self.device_mac = self.device[num]['macID']
        self.lineEdit_3.setText(self.device_mac)  # lineEdit_3属于mac
        self.lineEdit_6.setText(globalName.device_configModule)
        self.lineEdit_7.setText(globalName.device_cid)
        self.lineEdit_8.setText(globalName.device_uuid)

    def login(self):
        self.comboBox_2.clear()
        self.comboBox_4.clear()
        millis = int(round(time.time() * 1000))
        traceId = str(millis)
        user = self.lineEdit.text()
        password = self.lineEdit_2.text()
        data_user = {
            "email": "",
            "password": "",
            "registerTime": 0,
            "isRequiredVerify": True,
            "userType": "1",
            "traceId": "",
            "appVersion": "VeSync 3.0.56",
            "phoneOS": "Android 10",
            "acceptLanguage": "en",
            "method": "login",
            "phoneBrand": "CLT-AL01",
            "timeZone": "America/Phoenix",
            "debugMode": False
        }

        m = hashlib.md5()
        m.update(password.encode("utf-8"))
        if len(password) == 32:
            password_md5 = password
        else:
            password_md5 = m.hexdigest()
        data_user["email"] = user
        data_user["password"] = password_md5
        data_user["traceId"] = traceId
        if self.comboBox.currentText() == "联调环境":
            url = "https://test-online.vesync.com"
            globalName.device_url = url + "/cloud/v2/deviceManaged/bypassV2"
            self.url_user = url + "/cloud/v1/user/login"

        elif self.comboBox.currentText() == "预发布环境":
            url = "https://predeploy-smartapi.vesync.com"
            globalName.device_url = url + "/cloud/v2/deviceManaged/bypassV2"
            self.url_user = url + "/cloud/v1/user/login"

        elif self.comboBox.currentText() == "线上环境":
            url = "https://smartapi.vesync.com"
            globalName.device_url = url + "/cloud/v2/deviceManaged/bypassV2"
            self.url_user = url + "/cloud/v1/user/login"

        else:
            url = False

        logger.debug(" globalName.device_url %s" % globalName.device_url)
        if url:
            loginRes = commonFunc().gentoken(user, password_md5,self.url_user)
            print("【" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "】： 环境登录成功")

            hjson = json.loads(loginRes.text)
            globalName.device_token = hjson['result']['token']
            globalName.device_accountID = hjson['result']['accountID']

            logger.debug("【token：" +  globalName.device_token + "accountID：" + globalName.device_accountID + "】")
            # 获取设备列表
            devicesRes = commonFunc().getAppDevInfo(globalName.device_token, globalName.device_accountID)
            devices_list = json.loads(devicesRes.text)
            self.device = devices_list["result"]["list"]
            if len(self.device):
                for i in range(0, len(self.device)):
                    self.comboBox_2.addItem(self.device[i]["deviceName"])
            else:
                logger.error("设备为空")
            # 保存配置文件参数,需要读取配置，故此文件需要手动编辑，自动写入账号密码意义不大。--20220125 Eleven
            # self.cfg_save()
        else:
            logger.error(" login 环境选择错误")
        con = configparser.ConfigParser()
        con.read(setting.TEST_CONFIG, encoding='utf-8')
        sectionName = con.sections()
        logger.debug(sectionName)
        for i in range(2, len(sectionName)):
            self.comboBox_4.addItem(sectionName[i])

    def running(self):
        if self.pushButton.text() == "开始测试":

            globalName.deviceType = self.comboBox_3.currentIndex()
            logger.debug("deviceType --->%s" % globalName.deviceType)
            deviceNum = self.comboBox_4.currentIndex()

            globalName.testDevice = self.comboBox_4.itemText(deviceNum)
            logger.debug("全局变量testDevice--->%s" % globalName.testDevice)
            print("=============================================开始测试--设备类型：%s(0-炸锅/1-烤箱)=============================================" % globalName.deviceType)
            self.myThread = threading.Thread(target=self.excute_excel)
            self.myThread.setDaemon(True)
            self.myThread.start()
            self.pushButton.setText("停止测试")
        else:
            self._async_raise(self.myThread.ident, SystemExit)
            self.pushButton.setText("开始测试")
            print("=============================================停止测试=============================================")


    def outputWritten(self, text):  # 添加脚本执行结果到输出区
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def excute_excel(self):
        cases = addRunCase().add_case()
        addRunCase().run_case(cases)


    def _async_raise(self, tid, exc_type):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def Prepare_the_environment(self, device_url, data1):
        logger.debug(" Prepare_the_environment 执行预知条件....")
        conf = configparser.ConfigParser()  # 配置文件存在则加载
        conf.read("thirsparttest.ini", encoding="utf-8-sig")
        # 读取配置

        deviceinfo = {"traceId": "", "method": "bypass", "token": "", "accountID": "", "timeZone": "Asia/Shanghai",
                      "acceptLanguage": "en", "appVersion": "V3.0.8 build9", "phoneBrand": "iPhone 6s",
                      "phoneOS": "iOS 12.2", "debugMode": True, "pid": "wnxwqs76gknqyzjn", "cid": "",
                      "uuid": "6e3c1149-2ffe-48d5-8a23-09664e37e818",
                      "configModule": "", "jsonCmd": ""}

        self.device_url = globalName.device_url
        self.data1 = data1
        device_traceID = int(round(time.time() * 1000))
        try:
            while True:
                data1 = json.loads(data1)
                print("下发指令——", data1)
                deviceinfo["jsonCmd"] = data1
                deviceinfo["traceId"] = device_traceID
                deviceinfo["token"] = globalName.device_token
                deviceinfo["accountID"] = globalName.device_accountID
                deviceinfo["configModule"] = globalName.device_configModule
                deviceinfo["cid"] = globalName.device_cid
                print("deviceinfo——", deviceinfo)
                res = requests.post(self.device_url, json=deviceinfo, verify=False)
                print("设备回复——", json.loads(res.text))
                if json.loads(res.text)['code'] == 0:
                    print("结果：设备设置工作成功")
                    break
                else:
                    logger.error(" Prepare_the_environment 结果：设备设置工作失败")
        except Exception as e:
            logger.error(e)
            loop = QEventLoop()
            QTimer.singleShot(3000, loop.quit)
            loop.exec_()
            self.Prepare_the_environment(data1)


    def get_device_result(self, device_url, data1):
        logger.debug(" get_device_result 设备状态查询中....")
        self.device_url = globalName.device_url
        self.data1 = data1
        device_traceID = int(round(time.time() * 1000))
        try:
            while True:
                data1 = json.loads(data1)
                logger.debug("结果——读取:--> %s" % data1)
                data1["traceId"] = device_traceID
                data1["token"] = globalName.device_token
                data1["accountID"] = globalName.device_accountID
                data1["configModule"] = globalName.device_configModule
                data1["cid"] = globalName.device_cid

                logger.debug("结果——赋值:--> %s" % data1)
                res = requests.post(self.device_url, json=data1, verify=False)
                if json.loads(res.text)['code'] == 0:
                    logger.debug("结果：获取状态成功!")
                    return res.text
                else:
                    logger.error("结果：获取状态失败!")

        except Exception as e:
            logger.error(" get_device_result 异常! %s" % e)
            loop = QEventLoop()
            QTimer.singleShot(3000, loop.quit)
            loop.exec_()
            self.get_device_result(self, globalName.device_url, data1)

