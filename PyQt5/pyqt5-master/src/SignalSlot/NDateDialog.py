from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DateDialog(QDialog):
    def __init__(self,parent=None):
        super(DateDialog,self).__init__(parent)
        self.setWindowTitle("DateDialog")

        layout = QVBoxLayout(self)
        #日期编辑控件
        self.datetime = QDateTimeEdit(self)

        self.datetime.setCalendarPopup(True)
        #当前日期
        self.datetime.setDateTime(QDateTime.currentDateTime())

        layout.addWidget(self.datetime)
        #水平放置两按键
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
        #self.accept，self.reject系统提供
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def dateTime(self):
        print("fsdfafa")
        return self.datetime.dateTime()

    #静态方法
    @staticmethod
    def getDateTime(parent = None):
        dialog = DateDialog(parent)
        #显示对话框
        result = dialog.exec()
        date = dialog.dateTime()
        return (date.date(),date.time(),result == QDialog.Accepted)

