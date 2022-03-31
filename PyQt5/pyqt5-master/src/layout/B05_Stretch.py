'''

设置伸缩量（addStretch）

所以该函数的作用就是平分布局，它所带的参数就是所占的比例。
https://blog.csdn.net/wowocpp/article/details/105264371
'''

import sys,math
from PyQt5.QtWidgets import *


class Stretch(QWidget) :
    def __init__(self):
        super(Stretch,self).__init__()
        self.setWindowTitle("设置伸缩量")
        btn1 = QPushButton(self)
        btn2 = QPushButton(self)
        btn3 = QPushButton(self)
        btn1.setText("按钮1")
        btn2.setText("按钮2")
        btn3.setText("按钮3")

        layout = QHBoxLayout()

        #右中心对齐
        layout.addStretch(1)
        layout.addWidget(btn1)

        layout.addStretch(2)
        layout.addWidget(btn2)
        layout.addStretch(3)
        layout.addWidget(btn3)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Stretch()
    main.show()
    sys.exit(app.exec_())