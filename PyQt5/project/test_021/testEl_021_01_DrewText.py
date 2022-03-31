'''

绘图API：绘制文本

1. 文本
2. 各种图形（直线，点，椭圆，弧，扇形，多边形等）
3. 图像

QPainter
创建实列
painter = QPainter()
初始化
painter.begin()
绘制文本
painter.drawText(...)
结束
painter.end()


必须在paintEvent事件方法中绘制各种元素


'''

import sys
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QPainter,QColor,QFont
from PyQt5.QtCore import Qt

class DrawText(QWidget):
    def __init__(self):
        super(DrawText,self).__init__()
        self.setWindowTitle('在窗口上绘制文本')
        self.resize(500,500)
        self.text = "Python从菜鸟到高手"

    #在pycharm中使用paintEvent，内置使用a0关键字，其实这个关键字可以使用任意字符替换def paintEvent(self, a0:QtGui.QPaintEvent)：event-事件
    # def paintEvent(self, a0: QtGui.QPaintEvent):
    #     painter = QPainter(self)
    #     painter.begin(self)
    #     self.drawext(a0,painter)
    #     painter.end()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        #画笔
        painter.setPen(QColor(150,43,5))
        #字体
        painter.setFont(QFont('SimSun',25))
        #event.rect()区域：event整个区域；Qt.AlignCenter居中
        painter.drawText(event.rect(),Qt.AlignCenter,self.text)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawText()
    main.show()
    sys.exit(app.exec_())
