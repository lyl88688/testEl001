'''

单选按钮控件（QRadioButton）

'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QRadioButtonDemo(QWidget):
    def __init__(self):
        super(QRadioButtonDemo,self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('QRadioButton')
        layout = QHBoxLayout()
        self.button1 = QRadioButton('单选按钮1')

        # 将按钮1设为默认选中
        self.button1.setChecked(True)
        # 一般只有状态改变触发，则toggled信号更适合这种状态的监控
        self.button1.toggled.connect(self.buttonState)
        layout.addWidget(self.button1)

        self.button2 = QRadioButton('单选按钮2')
        self.button2.toggled.connect(self.buttonState)
        layout.addWidget(self.button2)
        self.setLayout(layout)


    def buttonState(self):
        radioButton = self.sender()#调用sender()方法可以判断发送信号的信号源是哪一个

        if radioButton.isChecked() == True:
            print('<' + radioButton.text() + '> 被选中')
        else:
            print('<' + radioButton.text() + '> 被取消选中状态')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QRadioButtonDemo()
    main.show()
    sys.exit(app.exec_())