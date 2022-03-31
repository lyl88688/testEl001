
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QFormLayout, QLabel, QLineEdit

'''
让控件支持拖拽动作 的案例
A.setDragEnabled(True)
B.setAcceptDrops(True)
B需要两个事件
1.dragEnterEvent  将A拖到B触发
2.dropEvent 在B的区域放下A时触发
'''


# 自定义控件
class MyComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e)
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())


class drawDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置定位和左上角坐标
        self.setGeometry(300, 300, 350, 220)
        # 设置窗口标题
        self.setWindowTitle('控件支持拖拽动作 的演示')
        # 设置窗口图标
        # self.setWindowIcon(QIcon('../web.ico'))
        formLayout = QFormLayout()
        formLayout.addRow(QLabel("请将左边的文本拖拽到右边的下拉列表中"))
        lineEdit = QLineEdit()
        # 设置可拖拽
        lineEdit.setDragEnabled(True)

        combo = MyComboBox()
        formLayout.addRow(lineEdit, combo)
        self.setLayout(formLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用图标
    app.setWindowIcon(QIcon('../web.ico'))
    w = drawDemo()
    w.show()
    sys.exit(app.exec_())

