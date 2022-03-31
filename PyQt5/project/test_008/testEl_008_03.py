

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
        labelAA = QLabel("Name")
        lineEditBB = QLineEdit("name")
        buttonCC = QPushButton("Submit")

        # 设置伸缩量为1
        # hlayout.addStretch(1)
        hlayout.addWidget(labelA)
        # hlayout.addStretch(1)
        hlayout.addWidget(lineEditB)
        # hlayout.addStretch(1)
        hlayout.addWidget(buttonC)
        # hlayout.addStretch(1)


        # hlayouttwo.addStretch(0)
        hlayouttwo.addWidget(labelAA)
        # hlayouttwo.addStretch(0)
        hlayouttwo.addWidget(lineEditBB)
        # hlayouttwo.addStretch(0)
        hlayouttwo.addWidget(buttonCC)
        # hlayouttwo.addStretch(0)

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






