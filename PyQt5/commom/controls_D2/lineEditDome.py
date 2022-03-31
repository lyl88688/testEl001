'''

QLineEdit综合案例

'''

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys



# 自定义控件
class MyComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e)
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())


class QLineEditDemo(QWidget):
    def __init__(self):
        super(QLineEditDemo,self).__init__()
        self.initUI()

    def initUI(self):
        edit1 = QLineEdit()
        # 使用int校验器
        edit1.setValidator(QIntValidator())
        edit1.setMaxLength(4)  # 不超过9999
        edit1.setAlignment(Qt.AlignRight)
        edit1.setFont(QFont('Arial',20))
        edit2 = QLineEdit()
        edit2.setValidator(QDoubleValidator(0.99,99.99,2))
        edit3 = QLineEdit()
        #输入限制
        edit3.setInputMask('99_9999_999999;#')
        edit4 = QLineEdit()
        edit4.textChanged.connect(self.textChanged)
        edit5 = QLineEdit()
        edit5.setEchoMode(QLineEdit.Password)
        edit5.editingFinished.connect(self.enterPress)
        edit6 = QLineEdit('Hello PyQt5')
        edit6.setReadOnly(True)
        edit7 = QLineEdit()
        combox = MyComboBox()
        #可拖拽
        edit7.setDragEnabled(True)
        edit8 = QLineEdit()
        edit8.setPlaceholderText("浮现文字！")
        edit9 = QLineEdit()
        edit9.setText("setFocus只能是首行")
        edit9.setFocus()
        edit9.selectAll()

        edit_num = QLineEdit()
        edit_num.setInputMask("000.000.000;_")
        edit_mac = QLineEdit("MAC")
        edit_mac.setInputMask("HH:HH:HH:HH:HH:HH;_")
        edit_date = QLineEdit("data")
        edit_date.setInputMask("0000-00-00")
        edit_str = QLineEdit("str")
        edit_str.setInputMask(">AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#")

        formLayout = QFormLayout()
        formLayout.addRow("setFocus首行", edit9)
        formLayout.addRow('整数校验&长度限制QIntValidator',edit1)
        formLayout.addRow('浮点数校验QDoubleValidator',edit2)
        formLayout.addRow('密码setEchoMode',edit5)
        formLayout.addRow('只读setReadOnly',edit6)
        formLayout.addRow(QLabel("请将左边的文本拖拽到右边的下拉列表中"))
        formLayout.addRow(edit7, combox)
        formLayout.addRow("浮显setPlaceholderText", edit8)
        formLayout.addRow('掩码Input Mask', edit3)
        formLayout.addRow("mnum", edit_num)
        formLayout.addRow("mac", edit_mac)
        formLayout.addRow("data", edit_date)
        formLayout.addRow("str", edit_str)
        formLayout.addRow('文本变化触发', edit4)



        self.setLayout(formLayout)
        self.setWindowTitle('QLineEdit综合案例')
    def textChanged(self,text):
        print('输入的内容：' + text)

    def enterPress(self):
        print('已输入值')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QLineEditDemo()
    main.show()
    sys.exit(app.exec_())