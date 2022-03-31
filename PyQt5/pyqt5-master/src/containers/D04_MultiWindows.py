'''

容纳多文档的窗口

QMdiArea

QMdiSubWindow

'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MultiWindows(QMainWindow):

    count = 0#记录窗口数量

    def __init__(self, parent=None):
        super(MultiWindows, self).__init__(parent)

        self.setWindowTitle("容纳多文档的窗口")
        #容纳多文档对象
        self.mdi = QMdiArea()
        #它将把widget设置为主窗口的中心窗口部件
        self.setCentralWidget(self.mdi)
        bar = self.menuBar()
        file = bar.addMenu("File")
        #新建
        file.addAction("New")
        #窗口方式：重叠
        file.addAction("cascade")
        #窗口方式：平铺
        file.addAction("Tiled")

        file.triggered.connect(self.windowaction)
    def windowaction(self,q):
        print(q.text())
        if q.text() == "New":
            MultiWindows.count = MultiWindows.count + 1
            #子窗口
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("子窗口" + str(MultiWindows.count))
            self.mdi.addSubWindow(sub)
            sub.show()
        elif q.text() == "cascade":
            self.mdi.cascadeSubWindows()
        elif q.text() == "Tiled":
            self.mdi.tileSubWindows()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MultiWindows()
    demo.show()
    sys.exit(app.exec_())