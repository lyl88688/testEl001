# from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLabel
import sys


#创建QApplocation类的实例（应用）；传入界面变量；
app = QApplication(sys.argv)
#创建窗口
window = QWidget()
#标题
window.setWindowTitle("Name")
#大小
window.resize(600, 500)
#按钮
btn = QPushButton(window)
btn.setText("按钮")
btn.resize(120, 30)
#使用move(x,y) 可以对窗口进行布局，即位置。
btn.move(100, 100)
btn.setStyleSheet('background-color:green;font-size:16px;')
#标签
label = QLabel()
label.setText('标签')
# label.setStyleSheet()
#显示窗口
label.show()
window.show()

#进入程序主循环，并通过exit函数确保安全退出。检测退出原因，安全退出code = 0;异常code = 1。无app.exec_()闪退。
sys.exit(app.exec_())