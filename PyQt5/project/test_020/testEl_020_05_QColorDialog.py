'''

颜色对话框：QColorDialog

'''


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class QColorDialogDemo(QWidget):
    def __init__(self):
        super(QColorDialogDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Color Dialog例子')
        layout = QVBoxLayout()
        self.colorButton = QPushButton('设置颜色')
        self.colorButton.clicked.connect(self.getColor)
        layout.addWidget(self.colorButton)

        self.colorButton1 = QPushButton('设置背景颜色')
        self.colorButton1.clicked.connect(self.getBGColor)
        layout.addWidget(self.colorButton1)

        self.colorLabel = QLabel('Hello，测试颜色例子')
        layout.addWidget(self.colorLabel)

        self.setLayout(layout)
    def getColor(self):
        #getColor()仅返回颜色一个值
        color = QColorDialog.getColor()
        #窗口调色板实例
        p = QPalette()

        #选择设置的对象：WindowText窗口部件前景色(文本颜色)（QPalette.Text、QPalette.ButtonText等等不同对象）
        p.setColor(QPalette.WindowText,color)
        self.colorLabel.setPalette(p)

    def getBGColor(self):
        color = QColorDialog.getColor()
        p = QPalette()
        # 选择设置的对象：Window窗口部件背景色
        p.setColor(QPalette.Window,color)

        #不加这句，则颜色不生效，设置自动填充为真
        self.colorLabel.setAutoFillBackground(True)
        self.colorLabel.setPalette(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QColorDialogDemo()
    main.show()
    sys.exit(app.exec_())

