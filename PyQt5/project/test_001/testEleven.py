
from PyQt5.QtWidgets import  QApplication,QMainWindow
import os,sys
from project.test_001.eleven import *


class MyMainFromEl(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainFromEl, self).__init__(parent)
        self.datalight = None

        self.setupUi(self)


if __name__=="__main__":
    #创建一个QApplication类的实列
    app=QApplication(sys.argv)
    #创建主窗口
    win=MyMainFromEl()
    #显示窗口
    win.show()
    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())