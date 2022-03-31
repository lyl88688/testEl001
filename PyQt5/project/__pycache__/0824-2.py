from  l210824 import  *
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow

class myWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        ui = Ui_MainWindow()
        ui.setupUi(self)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = myWindow()
    mainWindow.show()
    sys.exit(app.exec_())