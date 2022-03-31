"""
主窗口类型

有3种窗口

QMainWindow

QWidget

QDialog

QMainWindow：可以包含菜单栏、工具栏、状态栏和标题栏，是最常见的窗口形式

QDialog：是对话窗口的基类。没有菜单栏、工具栏、状态栏。

QWidget：不确定窗口的用途，就使用QWidget。


"""



import sys
#QMainWindow--创建主窗口；QApplication--创建主程序;QDesktopWidget--获取屏幕窗口;QWidget--窗口；QPushButton--按钮
from PyQt5.QtWidgets import QMainWindow,QApplication,QDesktopWidget,QWidget,QPushButton
#QIcon--创建图标
from PyQt5.QtGui import QIcon

#主窗口，继承QMainWindow
class FirstMainWin(QMainWindow):
    #初始化，将控件放在哪
    def __init__(self):
        super(FirstMainWin,self).__init__()

        # 设置主窗口的标题
        self.setWindowTitle('第一个主窗口应用')

        # 设置窗口的尺寸
        self.resize(400,600)

        #获取状态栏
        self.status = self.statusBar()

        self.status.showMessage('只存在5秒的消息',5000)


    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft,newTop)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('Dragon.ico'))

    main = FirstMainWin()

    main.show()

    sys.exit(app.exec_())
















