'''

让程序定时关闭

一定时间后调用
QTimer.singleShot

PyQt 动态 setWindowFlags
https://www.cnblogs.com/HenryZeng/p/13191927.html
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = QLabel('<font color=red size=140><b>Hello World，窗口在5秒后自动关闭!</b></font>')

    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    label.show()
    QTimer.singleShot(5000,app.quit)

    sys.exit(app.exec_())





    """
    PYQT基本窗口类型有如下类型：
    Qt.Qt.Widget#插件默认窗口，有最小化、最大化、关闭按钮
    Qt.Qt.Window#普通窗口，有最小化、最大化、关闭按钮
    Qt.Qt.Dialog#对话框窗口，有问号和关闭按钮
    Qt.Qt.Popup#弹出窗口，窗口无边框化
    Qt.Qt.ToolTip#提示窗口，窗口无边框化，无任务栏窗口
    Qt.Qt.SplashScreen#飞溅屏幕，窗口无边框化，无任务栏窗口
    Qt.Qt.SubWindow#子窗口，窗口无按钮但有标题栏
    
    自定义外观的顶层窗口标志：
    Qt.Qt.MSWindowsFixedSizeDialogHint#窗口无法调整大小
    Qt.Qt.FramelessWindowHint#窗口无边框化
    Qt.Qt.CustomizeWindowHint#有边框但无标题栏和按钮，不能移动和拖动
    Qt.Qt.WindowTitleHint#添加标题栏和一个关闭按钮
    Qt.Qt.WindowSystemMenuHint#添加系统目录和一个关闭按钮
    Qt.Qt.WindowMaximizeButtonHint#激活最大化和关闭按钮，禁止最小化按钮
    Qt.Qt.WindowMinimizeButtonHint#激活最小化和关闭按钮，禁止最大化按钮
    Qt.Qt.WindowMinMaxButtonsHint#激活最小化、最大化和关闭按钮，#相当于Qt.Qt.WindowMaximizeButtonHint|Qt.Qt.WindowMinimizeButtonHint
    Qt.Qt.WindowCloseButtonHint#添加一个关闭按钮
    Qt.Qt.WindowContextHelpButtonHint#添加问号和关闭按钮，像对话框一样
    Qt.Qt.WindowStaysOnTopHint#窗口始终处于顶层位置
    Qt.Qt.WindowStaysOnBottomHint#窗口始终处于底层位置
    """