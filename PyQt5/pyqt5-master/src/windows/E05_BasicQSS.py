'''

QSS基础

QSS（Qt Style Sheets）
Qt样式表

用于设置控件的样式/样式：背景色、字体大小等等

CSS

'''

from PyQt5.QtWidgets import *
import sys
class BasicQSS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSS样式")
        btn1 = QPushButton(self)
        btn1.setText("按钮1")
        btn2 = QPushButton(self)
        btn2.setText("按钮2")

        btn3 = QPushButton(self)
        btn3.setText("按钮3")

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        self.setLayout(vbox)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = BasicQSS()
    # 选择器：选择所有满足要求的，QPushButton为所有按键
    qssStyle = '''
        QPushButton {
            background-color:red
        }
    '''
    #窗口全局有效
    form.setStyleSheet(qssStyle)
    form.show()
    sys.exit(app.exec_())