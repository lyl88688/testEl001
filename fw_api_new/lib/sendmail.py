#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import setting
import smtplib
from lib.newReport import new_report
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(file_new):
    """
    定义发送邮件
    :param file_new:
    :return: 成功：打印发送邮箱成功；失败：返回失败信息
    """
    f = open(file_new,'rb')
    mail_body = f.read()
    f.close()
    #发送附件
    con = configparser.ConfigParser()
    con.read(setting.TEST_CONFIG, encoding='utf-8')
    report = new_report(setting.TEST_REPORT)
    sendfile = open(report,'rb').read()
    # --------- 读取config.ini配置文件 ---------------
    HOST = con.get("user","HOST_SERVER")
    SENDER = con.get("user","FROM")
    RECEIVER = con.get("user","TO")
    USER = con.get("user","user")
    PWD = con.get("user","password")
    SUBJECT = con.get("user","SUBJECT")

    att = MIMEText(sendfile,'base64','utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", report))

    msg = MIMEMultipart('related')
    msg.attach(att)
    msgtext = MIMEText(mail_body,'html','utf-8')
    msg.attach(msgtext)
    msg['Subject'] = SUBJECT
    msg['from'] = SENDER
    msg['to'] = RECEIVER
    print(RECEIVER.split(','))

    try:
        server = smtplib.SMTP(HOST)#创建一个SMTP()对象,传入HOST是因为python3.9版本差异，需要传入非空host。20210610
        server.connect(HOST)#通过connect 方法连接smtp主机
        server.starttls()#开启安全传输模式
        server.login(USER,PWD)
        server.sendmail(SENDER,RECEIVER.split(','),msg.as_string())
        server.quit()
        print("邮件发送成功！")

    except Exception as e:
        print("失败: " + str(e))


# send_mail(r"F:\02.KM\02.Software\002.Automatic\06.lyl_api_vesync\report\2021-06-08 19_30_14result.html")