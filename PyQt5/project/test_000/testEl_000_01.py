"""
    #创建一个QApplication类的实列
    app=QApplication(sys.argv)
    #创建主窗口
    win=MyMainFromEl()
    #显示窗口
    win.show()
    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())

QMain Window 窗口可以包含菜单栏、工具栏、状态栏和标题栏等，是最常见的窗口形式，是 GUI 程序的主窗口。
QDialog 是对话框的基类，对话框主要用来执行短期任务和与用户进行互动任务，有模态和非模态两种形式
QWidget 可以用作嵌入其他窗口。



"""



from PyQt5.QtWidgets import  QApplication,QMainWindow
import sys
from project.test_000 import untitled2

class MyMainFromEl(QMainWindow, untitled2.Ui_Form):
    def __init__(self, parent=None):
        super(MyMainFromEl, self).__init__(parent)


        self.setupUi(self)

if __name__=="__main__":
    #创建一个QApplication类的实列
    app=QApplication(sys.argv)
    #创建主窗口
    win=MyMainFromEl()
    #显示窗口
    win.show()
    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())