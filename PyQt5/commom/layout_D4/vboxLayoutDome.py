import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class QCheckBoxDemo(QWidget):
    def __init__(self):
        super(QCheckBoxDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('演示')

        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()
        self.buttonA = QPushButton("A")
        self.buttonB = QPushButton("B")
        self.buttonC = QPushButton("C")
        self.buttonD = QPushButton("D")
        self.buttonE = QPushButton("E")
        hlayout.setSpacing(50)

        hlayout.addWidget(self.buttonA)
        hlayout.addWidget(self.buttonB)
        hlayout.addWidget(self.buttonC)
        hlayout.addWidget(self.buttonD)
        hlayout.addWidget(self.buttonE)

        hlayout2 = QHBoxLayout()
        self.buttonF = QPushButton("F")
        self.buttonG = QPushButton("G")
        self.buttonH = QPushButton("H")
        self.buttonI = QPushButton("I")
        # addWidget(控件，控件所占比例，对齐方式)
        hlayout2.addWidget(self.buttonF,0, Qt.AlignLeft | Qt.AlignTop)
        hlayout2.addWidget(self.buttonG,1)
        hlayout2.addWidget(self.buttonH,3, Qt.AlignLeft | Qt.AlignBottom)
        hlayout2.addWidget(self.buttonI,4, Qt.AlignLeft | Qt.AlignBottom)

        vlayout3 = QHBoxLayout()
        self.buttonM = QPushButton("M")
        self.buttonN = QPushButton("N")
        #addStretch：在布局中添加空白，并把非空白内容顶到布局的尾部。从而实现按钮右下方
        vlayout3.addStretch(1)
        vlayout3.addWidget(self.buttonM)
        vlayout3.addWidget(self.buttonN)

        vlayout4 = QHBoxLayout()
        self.buttonQ = QPushButton("Q")
        self.buttonW = QPushButton("W")
        vlayout4.addWidget(self.buttonQ)
        vlayout4.addWidget(self.buttonW)

        vlayout.addLayout(hlayout)
        #不能与对齐方式共存
        # vlayout.addStretch(200)
        vlayout.addLayout(hlayout2)
        vlayout.addLayout(vlayout3)
        vlayout.addStretch(200)
        vlayout.addLayout(vlayout4)

        self.setLayout(vlayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QCheckBoxDemo()
    main.show()
    sys.exit(app.exec_())