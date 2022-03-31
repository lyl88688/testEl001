'''

显示列表数据（QListView控件）
字符串类型
https://codingdict.com/sources/py/PyQt5.QtCore/9165.html
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

        listview = QListView()
        #数据源
        """
        我们这里使用了一个QListView来和 QStringListModel进行连接，这样 QStringListModel的内容就会在QListView中显示出来，
        任何对QStringListModel的修改都会显示在QListView中。这样我们就可以达到数据存储和显示的分离，
        我们可以专注我们的数据部分（QStringListModel，只要我们定义好接口），显示的部分就由QListView去负责，
        这就是QT的MVC（Model-View-Controller）机制，在MFC里也就是document和view。
        """
        listModel = QStringListModel()
        self.list = ["列表项1","列表项2", "列表项3"]

        listModel.setStringList(self.list)

        listview.setModel(listModel)
        listview.clicked.connect(self.clicked)
        layout.addWidget(listview)

        self.setLayout(layout)

    def clicked(self,item):
        QMessageBox.information(self,"QListView","您选择了：" + self.list[item.row()])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())
