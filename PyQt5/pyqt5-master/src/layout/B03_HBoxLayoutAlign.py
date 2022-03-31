'''

设置控件的对齐方式



'''

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class HBoxLayoutAlign(QWidget) :
    def __init__(self):
        super(HBoxLayoutAlign,self).__init__()
        self.setWindowTitle("水平盒布局")

        hlayout = QHBoxLayout()
        #addWidget(控件，控件所占比例，对齐方式)
        hlayout.addWidget(QPushButton('按钮1'),2,Qt.AlignLeft | Qt.AlignTop)
        hlayout.addWidget(QPushButton('按钮2'),4,Qt.AlignLeft | Qt.AlignTop)
        hlayout.addWidget(QPushButton('按钮3'),1)
        hlayout.addWidget(QPushButton('按钮4'),5,Qt.AlignLeft | Qt.AlignBottom)
        hlayout.addWidget(QPushButton('按钮5'),1,Qt.AlignLeft | Qt.AlignBottom)
        hlayout.setSpacing(40)
        self.setLayout(hlayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = HBoxLayoutAlign()
    main.show()
    sys.exit(app.exec_())