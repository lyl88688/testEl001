import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QComboBoxDemo(QWidget):
    def __init__(self):
        super(QComboBoxDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('下拉列表控件演示')
        self.resize(300,100)

        layout = QVBoxLayout()

        self.label = QLabel('请选择编程语言')

        self.cb = QComboBox()
        self.cb.addItem('C++')
        self.cb.addItem('Python')
        self.cb.addItems(['Java','C#','Ruby'])

        #当下拉选项的索引发生改变时发射该信号
        self.cb.currentIndexChanged.connect(self.selectionChange)
        #当用户选中一个下拉选项时发射该信号
        self.cb.activated.connect(self.activatetest)
        #当选中一个已经选中的下拉选项时，发射该信号（即鼠标移至某项）
        self.cb.highlighted.connect(self.highlightedtest)

        layout.addWidget(self.label)
        layout.addWidget(self.cb)

        self.setLayout(layout)

    def selectionChange(self,i):
        print(self.cb.currentText())
        self.label.setText(self.cb.currentText())
        self.label.adjustSize()
        print(self.cb.count())
        for count in range(self.cb.count()):
            print('item' + str(count) + ' = ' + self.cb.itemText(count))

        print('current index',i,'selection changed', self.cb.currentText())

    def  highlightedtest(self):
        print("当选中一个已经选中的下拉选项时，发射该信号（即鼠标移至某项）")

    def activatetest(self):
        print("当用户选中一个下拉选项时发射该信号(选中某个)")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QComboBoxDemo()
    main.show()
    sys.exit(app.exec_())