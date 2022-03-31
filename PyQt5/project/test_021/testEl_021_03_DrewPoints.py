'''

用像素点绘制正弦曲线

-2PI  2PI

drawPoint(x,y)

'''

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class DrawPoints(QWidget):
    def __init__(self):
        super(DrawPoints,self).__init__()
        self.resize(300,300)
        self.setWindowTitle('在窗口上用像素点绘制2个周期的正弦曲线')

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        #使用具体颜色定义或使用painter.setPen(QColor(150,43,5))
        painter.setPen(Qt.blue)
        #获取窗口尺寸
        size = self.size()

        for i in range(1000):
            #以窗口宽度/2为横坐标中心:即50+0.2倍数
            x = 100 * (-1 + 2.0 * i/1000) + size.width()/2.0
            # print(x)
            #math.sin((x - size.width()/2.0)   x对应正玄值，math.pi：Π（3.141592653......） 数值大小决定周期
            y = -50 * math.sin((x - size.width()/2.0) * math.pi/50) + size.height()/2.0

            # y = -50 * math.sin((x - size.width()/2.0) /5) + size.height()/2.0
            # print(y,-50 * math.sin((x - size.width()/2.0) * math.pi/50))
            print(x,y)
            #size.width()/2.0--size.height()/2.0:往右往下移，起点（50，150）
            painter.drawPoint(x,y)

        painter.end()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawPoints()
    main.show()
    sys.exit(app.exec_())