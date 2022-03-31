'''

信号（Signal）与槽（Slot）

信号：相当于事件，需要触发。
槽：函数或者方法，接收信号的工具或者代码。（发出信号，槽执行）

实现信号与槽之间的通讯
'''
from PyQt5.QtWidgets import *
import sys

class SigalSlotDemo(QWidget):
    def __init__(self):
        super(SigalSlotDemo,self).__init__()
        self.initUI()

    def onClick(self):
        self.btn.setText("信号已经发出")
        #样式
        self.btn.setStyleSheet("QPushButton(max-width:200px;min-width:200px")

    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('信号（Signal）与槽（Slot）')
        self.btn = QPushButton('我的按钮',self)
        #clicked-信号；self.onClick-方法（槽）
        self.btn.clicked.connect(self.onClick)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SigalSlotDemo()
    gui.show()
    sys.exit(app.exec_())