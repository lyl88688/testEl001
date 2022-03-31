"""

        # 总结发现,addLayout和addWidget是用来管理布局的
        # 而setLayout是将已设置好的布局应用到控件中去.

在PyQt5中，提供了三种窗口类型，QMainWindow，QWidget和QDialog，三个类都是用来
创建窗口的，可以直接使用，也可以继承后再使用

QMainWindow：包含菜单栏，工具栏，状态栏和标题栏。是最常见的窗口形式，通常被用

作为主窗口(不能设置布局，使用setLayout()方法，因为它有自己的布局)；
QDialog：是对话框窗口的基类。对话框主要用来执行短期任务，或者与用户进行互动，有
模态与非模态。这个窗口没有菜单栏，工具栏等
QWidget不清楚窗口用途时，使用QWidget类
QMainWindow继承自QWidget类，拥有它的派生方法和属性


"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QHBoxLayout, QWidget, QPushButton,QVBoxLayout,QLabel,QLineEdit
from PyQt5.QtGui import QIcon

class myMainWin(QWidget):
    def __init__(self, parent=None):
        super(myMainWin, self).__init__(parent)
        #水平布局
        hlayout = QHBoxLayout()
        #垂直布局
        hlayouttwo = QVBoxLayout()
        labelA = QLabel("Name")
        lineEditB = QLineEdit("name")
        buttonC = QPushButton("Submit")

        # 设置伸缩量为1
        hlayout.addWidget(labelA)
        hlayout.addWidget(lineEditB)
        hlayout.addWidget(buttonC)
        hlayouttwo.addWidget(labelA)
        hlayouttwo.addWidget(lineEditB)
        hlayouttwo.addWidget(buttonC)
        hwg = QWidget()  # 准备2个部件
        vwg = QWidget()

        hwg.setLayout(hlayout)
        vwg.setLayout(hlayouttwo)
        # """
        # 总结发现,addLayout和addWidget是用来管理布局的
        # 而setLayout是将已设置好的布局应用到控件中去.
        # """
        wlayout = QHBoxLayout()
        wlayout.addWidget(vwg)
        wlayout.addWidget(QPushButton(str(1)))

        wlayout.addWidget(hwg)
        # self.setCentralWidget(wlayout)
        self.setLayout(wlayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = myMainWin()

    win.show()

    sys.exit(app.exec_())






