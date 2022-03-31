from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QIcon, QPixmap

import sys


class WindowClass(QWidget):
    def __init__(self, parent=None):
        super(WindowClass, self).__init__(parent)
        self.btn_1 = QPushButton("Btn_1")
        self.btn_2 = QPushButton("Btn_2")
        self.btn_4 = QPushButton("Btn_4")

        # 快捷建设置，ALT+大写首字母
        self.btn_3 = QPushButton("&DownLoad")
        self.btn_1.setText('First Button1')
        self.btn_1.setCheckable(True)  # 设置已经被点击
        self.btn_1.toggle()  # 切换按钮状态
        self.btn_1.clicked.connect(self.btnState)
        self.btn_1.clicked.connect(lambda: self.wichBtn(self.btn_1))

        self.btn_2.setIcon(QIcon(QPixmap('./python.jpg')))
        self.btn_2.setEnabled(False)  # 设置不可用状态
        self.btn_2.clicked.connect(lambda: self.wichBtn(self.btn_2))

        self.btn_3.setDefault(True)  # 设置该按钮式默认状态的
        self.btn_3.clicked.connect(lambda: self.wichBtn(self.btn_3))
        self.btn_4.clicked.connect(lambda: self.wichBtn(self.btn_4))

        self.resize(400, 300)
        layout = QVBoxLayout()
        layout.addWidget(self.btn_1)
        layout.addWidget(self.btn_2)
        layout.addWidget(self.btn_3)
        layout.addWidget(self.btn_4)

        self.setLayout(layout)


    def btnState(self):
        if self.btn_1.isChecked():
            print("Btn_1被单击")
        else:
            print("Btn_1未被单击")


    def wichBtn(self, btn):
        print("点击的按钮是：", btn.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())