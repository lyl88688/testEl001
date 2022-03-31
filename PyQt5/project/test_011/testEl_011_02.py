

# from PyQt5.QtWidgets import QApplication,QMainWindow,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,QPushButton,QWidget
from PyQt5 import QtWidgets
from project.test_011.untitled import *

import sys
from PyQt5.QtGui import QIcon

class myMainWin(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(myMainWin, self).__init__(parent)
        self.setupUi(self)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = myMainWin()
    win.show()
    sys.exit(app.exec_())





















