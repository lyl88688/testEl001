'''

显示列表数据（QListView控件）

'''

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView, QMessageBox
from PyQt5.QtCore import QStringListModel
import sys


class ListViewDemo(QWidget):
    def __init__(self, parent=None):
        super(ListViewDemo, self).__init__(parent)
        self.setWindowTitle("QListView 例子")
        self.resize(300, 270)
        layout = QVBoxLayout()

        #创建控件
        listview = QListView()
        #字符串列表模型，数据源，封装列表数据源--空模型
        listModel = QStringListModel()
        self.list = ["列表项1","列表项2", "列表项3"]


        listModel.setStringList(self.list)
        #模型与控件关联
        listview.setModel(listModel)
        listview.clicked.connect(self.clicked)


        layout.addWidget(listview)

        self.setLayout(layout)

    #单击的是对象item
    def clicked(self,item):
        #self.list[item.row()] 当前单击索引

        QMessageBox.information(self,"QListView","您选择了：" + self.list[item.row()])

    def display(self, i):
        # 设置当前可见的选项卡的索引
        print(i)
        # self.stack.setCurrentIndex(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())
