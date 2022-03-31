'''

复选框控件（QCheckBox）

3种状态

未选中：0

半选中：1

选中：2

'''

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
        self.checkBox1.stateChanged.connect(lambda:self.checkboxState(self.checkBox1))
        layout.addWidget(self.checkBox1)

        self.checkBox2 = QCheckBox('复选框控件2')
        self.checkBox2.stateChanged.connect(lambda:self.checkboxState(self.checkBox2))
        layout.addWidget(self.checkBox2)

        self.checkBox3 = QCheckBox('半选中')
        self.checkBox3.stateChanged.connect(lambda:self.checkboxState(self.checkBox3))
        """
        tristate属性表示复选框是三种状态还是两种状态，如果tristate为True，则表示复选框有选中、未选中和半选中三种状态，如果tristate为False，则表示复选框只有选中、未选中两种状态。

        复选框的ischecked（）方法在选中和半选中状态下都返回True。半选中状态一般用于复选框对应选择内容包含多个，例如Excel刷选数据时，全选是选择所有数据，未选择则是一条数据也没有，在二者之间的状态为半选中状态。

        tristate属性缺省为False，可以通过isTristate()、setTristate(bool y = true)进行读取和设置。
        """
        # self.checkBox3.setTristate(True)
        #PartiallyChecked部分选择，unchecked未选中，checked选中
        self.checkBox3.setCheckState(Qt.PartiallyChecked)
        layout.addWidget(self.checkBox3)

        self.setLayout(layout)

    def checkboxState(self,cb):
        check1Status = self.checkBox1.text() + ', isChecked=' + str(self.checkBox1.isChecked()) + ',checkState=' + str(self.checkBox1.checkState()) + '\n'
        check2Status = self.checkBox2.text() + ', isChecked=' + str(self.checkBox2.isChecked()) + ',checkState=' + str(self.checkBox2.checkState()) + '\n'
        check3Status = self.checkBox3.text() + ', isChecked=' + str(self.checkBox3.isChecked()) + ',checkState=' + str(self.checkBox3.checkState()) + '\n'
        print(check1Status + check2Status + check3Status)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QCheckBoxDemo()
    main.show()
    sys.exit(app.exec_())