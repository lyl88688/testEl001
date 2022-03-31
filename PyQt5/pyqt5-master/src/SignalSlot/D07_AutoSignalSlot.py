'''
信号与槽自动连接

规则：
on_objectname_signalname
on_okButton_clicked

第一步：槽注释
@QtCore.pyqtSlot()
第二步：按键另起名
self.okButton.setObjectName("okButton")
第三步：槽满足规则
on_objectname_signalname
第四步：调用以下方法，完成自动关联。
QtCore.QMetaObject.connectSlotsByName(self)

'''

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication ,QWidget ,QHBoxLayout , QPushButton
import sys

class AutoSignalSlot(QWidget):
    def __init__(self):
        super(AutoSignalSlot,self).__init__()
        self.okButton = QPushButton("ok",self)
        #给button设置名字，名称后面取用。on_objectname_signalname
        self.okButton.setObjectName("okButton")
        self.okButton1 = QPushButton("cancel",self)
        self.okButton1.setObjectName("cancelButton")
        layout = QHBoxLayout()
        layout.addWidget(self.okButton)
        self.setLayout(layout)
        #第三统一调用此方法
        QtCore.QMetaObject.connectSlotsByName(self)
        #self.okButton.clicked.connect(self.on_okButton_clicked)

    #QtCore.pyqtSlot()用于标注以下函数为槽

    @QtCore.pyqtSlot()
    def on_okButton_clicked(self):
        print("点击了ok按钮")

    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        print("点击了cancel按钮")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = AutoSignalSlot()
    example.show()
    sys.exit(app.exec_())