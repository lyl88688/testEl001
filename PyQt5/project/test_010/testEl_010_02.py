

# from PyQt5.QtWidgets import QApplication,QMainWindow,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,QPushButton,QWidget
from PyQt5 import QtWidgets

import sys
from PyQt5.QtGui import QIcon

class myMainWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(myMainWin, self).__init__(parent)
        self.resize(300, 100)
        formlayout = QtWidgets.QFormLayout()

        labelname = QtWidgets.QLabel("Name")
        labelage = QtWidgets.QLabel("Age")
        labelclass = QtWidgets.QLabel("Class")

        lineEditname = QtWidgets.QLineEdit()
        lineEditage = QtWidgets.QLineEdit()
        lineEditclass = QtWidgets.QLineEdit()
        buttonA = QtWidgets.QPushButton("确认")

        hlayout = QtWidgets.QVBoxLayout()
        hlayout.addWidget(lineEditclass)
        hlayout.addWidget(buttonA)



        formlayout.addRow(labelname, lineEditname)
        formlayout.addRow(labelage, lineEditage)
        formlayout.addRow(labelclass, hlayout)

        #
        """
        默认DontWrapRows该参数的含义是文本框总是出现在标签的后面，其中标签被赋予足够的水平空间以适应表单中出现的最宽的标签，其余的空间被赋予文本框。
        
        """
        # formlayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.DontWrapRows)

        """
        该参数通常适用于小屏幕中，当标签和文本框在屏幕的当前行显示不全时，文本框会显示在下一行，使得标签独占一行。
        """
        formlayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapLongRows)

        """
        该参数表示标签总是在文本框的上一行。
        """
        # formlayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)


        self.setLayout(formlayout)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = myMainWin()
    win.show()

    sys.exit(app.exec_())





















