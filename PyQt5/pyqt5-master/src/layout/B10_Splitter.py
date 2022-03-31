'''

拖动控件之间的边界（QSplitter）

pyqt5-QFrame边框样式
https://blog.csdn.net/weixin_30381317/article/details/97860276

'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Splitter(QWidget):
    def __init__(self):
        super(Splitter, self).__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        self.setWindowTitle('QSplitter 例子')
        self.setGeometry(300, 300, 300, 200)

        topleft = QFrame()
        #设置类型：绘制一个举行面板
        topleft.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        #拖动控件：水平
        splitter1 = QSplitter(Qt.Horizontal)
        textedit = QTextEdit()
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        #默认左右占比
        splitter1.setSizes([200,100])

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)


        hbox.addWidget(splitter2)
        self.setLayout(hbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Splitter()
    demo.show()
    sys.exit(app.exec_())

