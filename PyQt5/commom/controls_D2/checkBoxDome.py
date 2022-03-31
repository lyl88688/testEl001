import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class QCheckBoxDemo(QWidget):
    def __init__(self):
        super(QCheckBoxDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('复选框控件演示')

        layout = QHBoxLayout()

        self.checkBox1 = QCheckBox('复选框控件1')
        #默认选择
        self.checkBox1.setChecked(True)
        st = lambda: self.checkboxState(self.checkBox1)
        self.checkBox1.stateChanged.connect(st)
        layout.addWidget(self.checkBox1)

        self.checkBox2 = QCheckBox('复选框控件2')
        st2 = lambda: self.checkboxState(self.checkBox1)
        self.checkBox2.stateChanged.connect(st2)
        layout.addWidget(self.checkBox2)

        self.checkBox3 = QCheckBox('半选中')
        st3 = lambda: self.checkboxState(self.checkBox3)
        self.checkBox3.stateChanged.connect(self.printf)
        #PartiallyChecked部分选择，unchecked未选中，checked选中
        self.checkBox3.setCheckState(Qt.PartiallyChecked)
        layout.addWidget(self.checkBox3)

        self.setLayout(layout)

    def printf(self):
        print("ddfsfsd")
        check1Status = self.checkBox1.text() + ', isChecked=' + str(self.checkBox1.isChecked()) + ',checkState=' + str(
            self.checkBox1.checkState()) + '\n'
        check2Status = self.checkBox2.text() + ', isChecked=' + str(self.checkBox2.isChecked()) + ',checkState=' + str(
            self.checkBox2.checkState()) + '\n'
        check3Status = self.checkBox3.text() + ', isChecked=' + str(self.checkBox3.isChecked()) + ',checkState=' + str(
            self.checkBox3.checkState()) + '\n'

        print(check1Status + check2Status + check3Status)

    def checkboxState(self,bc):
        print(bc)
        check1Status = self.checkBox1.text() + ', isChecked=' + \
                       str(self.checkBox1.isChecked()) + ',checkState=' + \
                       str(self.checkBox1.checkState()) + '\n'
        check2Status = self.checkBox2.text() + ', isChecked=' + \
                       str(self.checkBox2.isChecked()) + ',checkState=' + \
                       str(self.checkBox2.checkState()) + '\n'
        check3Status = self.checkBox3.text() + ', isChecked=' + \
                       str(self.checkBox3.isChecked()) + ',checkState=' + \
                       str(self.checkBox3.checkState()) + '\n'
        print(check1Status + check2Status + check3Status)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QCheckBoxDemo()
    main.show()
    sys.exit(app.exec_())