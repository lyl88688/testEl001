#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os,sys
sys.path.append(os.path.dirname(__file__))
from lib.mainWidget import *


if __name__ =="__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())




