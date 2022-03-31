'''

文件对话框：QFileDialog
常用功能：打开文件、保存文件

getopenfilename():

返回用户所选择文件的名称并打开该文件
getsavefilename():

使用用户选择的文件名并保存文件
例：qfiledialog.getopenfilename(self,‘open file',‘d:\',‘image files(*.jpg *.png)')

第一个参数是指定父窗口
第二个参数是标题
第三个是默认打开目录，使用.代表当前目录
第四个是文件扩展名过滤器表示只能显示扩展名为.jpg和.png的文件
setfilemode():

可以选择的文件类型，没举型常量：
qfiledialog.anyfile-任何文件
qfiledialog.existingfile-已存在的文件
qfiledialog.directory-文件目录
qfiledialog.existingfiles-已存在的多个文件
setfilter():

设置过滤器，只显示过滤器允许的文件类型


'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QFileDialogDemo(QWidget):
    def __init__(self):
        super(QFileDialogDemo,self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.button1 = QPushButton('加载图片')
        self.button1.clicked.connect(self.loadImage)
        layout.addWidget(self.button1)

        self.imageLabel = QLabel()
        layout.addWidget(self.imageLabel)

        self.button2 = QPushButton('加载文本文件')
        self.button2.clicked.connect(self.loadTxt)
        layout.addWidget(self.button2)

        self.contents = QTextEdit()
        layout.addWidget(self.contents)

        #laodTxt与loadText对比
        self.button3 = QPushButton('加载文本文件2')
        self.button3.clicked.connect(self.loadText)
        layout.addWidget(self.button3)

        self.contents1 = QTextEdit()
        layout.addWidget(self.contents1)




        self.setLayout(layout)
        self.setWindowTitle('文件对话框演示 ')

    def loadImage(self):
        #getOpenFileName（self,对话框名称，默认路劲，过滤条件-打开文件类型） "_"不需要
        fname,_ = QFileDialog.getOpenFileName(self,'打开文件','.','图像文件(*.jpg *.png)')
        #设置文件扩展名过滤,注意用双分号间隔
        # fname,_ = QFileDialog.getOpenFileName(self,'打开文件','.', "All Files (*);;Text Files (*.txt)")
        #Label中显示图片：setPixmap
        self.imageLabel.setPixmap(QPixmap(fname))

    def loadTxt(self):
        #getOpenFileName（self,对话框名称，默认路劲，过滤条件-打开文件类型） "_"不需要
        fname,_ = QFileDialog.getOpenFileName(self,'打开文件','./','All Files (*)')
        #设置文件扩展名过滤,注意用双分号间隔
        print(fname)
        f = open(fname, encoding='utf-8', mode='r')
        # with语句的优势：with用完之后，会自动调用close函数，关闭文件。
        with f:
            data = f.read()
            self.contents.setText(data)

    def loadText(self):
        dialog = QFileDialog()
        #设置文件格式：#设置可以打开任何文件
        dialog.setFileMode(QFileDialog.AnyFile)
        #文件过滤
        dialog.setFilter(QDir.Files)

        #dialog.exec()显示对话框
        if dialog.exec():
            # 接受选中文件的路径，默认为列表
            filenames = dialog.selectedFiles()
            # 列表中的第一个元素即是文件路径，以只读的方式打开文件
            f = open(filenames[0],encoding='utf-8',mode='r')
            #with语句的优势：with用完之后，会自动调用close函数，关闭文件。
            with f:
                data = f.read()
                self.contents.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QFileDialogDemo()
    main.show()
    sys.exit(app.exec_())


