'''

按钮控件（QPushButton）

#控件类方法
QAbstractButton

QPushButton
AToolButton
QRadioButton
QCheckBox


'''


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QPushButtonDemo(QDialog) :
    def __init__(self):
        super(QPushButtonDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QPushButton Demo')

        layout = QVBoxLayout()
        #初始，设置按钮名称为'第1个按钮'
        self.button1 = QPushButton('第1个按钮')
        self.button1.setToolTip('这是第一个按钮，Are you ok？')

        #设置按钮名称，将上面设置默认值修改
        self.button1.setText('First Button1')

        #与toggle配合使用，表示可复选的状态
        self.button1.setCheckable(True)
        #toggle按钮按下后不会自动抬起，选中checkable后，Button变成切换按钮(toggle button)，可以有两种状态：按下/弹起
        self.button1.toggle()

        #与槽关联
        self.button1.clicked.connect(self.buttonState)
        self.button1.clicked.connect(lambda :self.whichButton(self.button1))

        layout.addWidget(self.button1)

        # 在文本前面显示图像

        self.button2 = QPushButton('图像按钮')
        # self.button2.setDefault(True)
        self.button2.setIcon(QIcon(QPixmap('./images/python.png')))
        self.button2.clicked.connect(lambda:self.whichButton(self.button2))
        layout.addWidget(self.button2)

        self.button3 = QPushButton('不可用的按钮')
        self.button3.setEnabled(False)
        layout.addWidget(self.button3)

        #设定快捷方式，使用alt + 单词首字母：alt + M 实现快速
        self.button4 = QPushButton('&MyButton')
        #使用setDefault（）方法·来设置按钮的默认状态。快捷键是‘&+文本’（&Download），通过‘Alt+M’快捷键来调用槽函数
        self.button4.setDefault(True)
        self.button4.clicked.connect(lambda:self.whichButton(self.button4))
        layout.addWidget(self.button4)

        self.setLayout(layout)
        self.resize(400,300)

    def buttonState(self):
        if self.button1.isChecked():
            print('按钮1已经被选中')
        else:
            print('按钮1未被选中')

    def whichButton(self,btn):
        print('被单击的按钮是<' + btn.text() + '>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QPushButtonDemo()
    main.show()
    sys.exit(app.exec_())
