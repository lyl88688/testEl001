

# from PyQt5.QtWidgets import QApplication,QMainWindow,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,QPushButton,QWidget
from PyQt5 import QtWidgets

import sys
from PyQt5.QtGui import QIcon

class myMainWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(myMainWin, self).__init__(parent)
        self.resize(300, 200)
        gridlayout = QtWidgets.QGridLayout()

        labelname = QtWidgets.QLabel("Name")
        labelage = QtWidgets.QLabel("Age")
        labelclass = QtWidgets.QLabel("Class")

        lineEditname = QtWidgets.QLineEdit()
        lineEditage = QtWidgets.QTextEdit()
        lineEditclass = QtWidgets.QComboBox()

        gridlayout.addWidget(labelname,1,0)
        gridlayout.addWidget(lineEditname,1,1)

        gridlayout.addWidget(labelclass,2,0)
        gridlayout.addWidget(lineEditclass,2,1)
        gridlayout.addWidget(labelage,3,0)
        gridlayout.addWidget(lineEditage,3,1)
        self.setLayout(gridlayout)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = myMainWin()
    win.show()

    sys.exit(app.exec_())





















