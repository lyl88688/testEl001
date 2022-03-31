import sys
from PyQt5.QtWidgets import QHBoxLayout,QMainWindow,QApplication,QPushButton,QWidget

class QuitApplication(QMainWindow):
    def __init__(self):
        super(QuitApplication,self).__init__()
        self.resize(300,120)
        self.setWindowTitle('退出应用程序')

        # 添加Button

        self.button1 = QPushButton('退出应用程序')
        # 将信号与槽关联
        self.button1.clicked.connect(self.onClick_Button)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        #将layout放到窗口
        mainFrame.setLayout(layout)

        #将mainFrame放入主窗口
        self.setCentralWidget(mainFrame)

    # 按钮单击事件的方法（自定义的槽）
    def onClick_Button(self):
        # 调用sender()方法可以判断发送信号的信号源是哪一个：发送信号的对象
        sender = self.sender()
        print(sender.text() + ' 按钮被按下')

        #得到一个实列-instance（实列）
        app = QApplication.instance()
        # 退出应用程序
        app.quit()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QuitApplication()
    main.show()
    sys.exit(app.exec_())