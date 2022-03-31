'''

多线程更新UI数据（在两个线程中传递数据）

另外一个线程中完成任务，且触发信号，信号关联槽函数。

衍生：多个线程之间传递数据
'''

from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit
import time
import sys

#线程
class BackendThread(QThread):
    update_date = pyqtSignal(str)

    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currentTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currentTime))
            time.sleep(1)

class ThreadUpdateUI(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('多线程更新UI数据')
        self.resize(400,100)
        self.input = QLineEdit(self)
        self.input.resize(400,100)

        self.initUI()
    def initUI(self):
        self.backend = BackendThread()
        self.backend.update_date.connect(self.handleDisplay)

        #启动线程
        self.backend.start()

    def handleDisplay(self,data):
        self.input.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = ThreadUpdateUI()
    example.show()
    sys.exit(app.exec_())