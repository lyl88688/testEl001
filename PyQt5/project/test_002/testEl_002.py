

from PyQt5.QtWidgets import QApplication,QMainWindow
from project.test_002.elevenUi import *
import sys

class myMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(myMainWindow, self).__init__(parent)

        self.setupUi(self)





if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = myMainWindow()

    win.show()

    sys.exit(app.exec_())






