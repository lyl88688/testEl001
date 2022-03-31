'''

对话框：QDialog

QMessageBox:显示消息对话框
QColorDialog：显示颜色对话框
QFileDialog：文件打开，保存对话框
QFontDialog：设置 字体
QInputDialog：获取用户输入信息


窗口：
QMainWindow
QWidget
QDialog

'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QDialogDemo(QMainWindow):
    def __init__(self):
        super(QDialogDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QDialog案例')
        self.resize(300,200)

        self.button = QPushButton(self)
        self.button.setText('弹出对话框')
        self.button.move(50,50)
        self.button.clicked.connect(self.showDialog)

    def showDialog(self):
        #创建对话框实例
        dialog = QDialog()
        #dialog中放置按钮
        button = QPushButton('确定',dialog)
        #绑定到dialog.close槽
        button.clicked.connect(dialog.close)
        button.move(50,50)
        dialog.setWindowTitle('对话框')
        #以模式状态显示：打开状态下，主窗口不可用。
        dialog.setWindowModality(Qt.ApplicationModal)
        # 显示对话框
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialogDemo()
    main.show()
    sys.exit(app.exec_())

