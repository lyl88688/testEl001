'''

停靠控件（QDockWidget）
悬浮窗口


'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DockDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DockDemo, self).__init__(parent)

        self.setWindowTitle("停靠控件（QDockWidget）")

        layout = QHBoxLayout()
        self.items = QDockWidget('Dockable',self)
        self.listWidget = QListWidget()
        self.listWidget.addItem('item1')
        self.listWidget.addItem('item2')
        self.listWidget.addItem('item3')

        self.items.setWidget(self.listWidget)
        #中间区域增加可编辑窗口，效果更加明显。
        self.setCentralWidget(QLineEdit())

        #s是否悬浮，默认不悬浮。
        self.items.setFloating(True)
        #Qt.RightDockWidgetArea 停靠区域
        self.addDockWidget(Qt.RightDockWidgetArea,self.items)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DockDemo()
    demo.show()
    sys.exit(app.exec_())
