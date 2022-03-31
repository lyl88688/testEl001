'''

添加、修改和删除树控件中的节点

#节点可编辑
root.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
https://blog.csdn.net/lly1122334/article/details/103031843
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class ModifyTree(QWidget):
    def __init__(self, parent=None):
        super(ModifyTree, self).__init__(parent)
        self.setWindowTitle('TreeWidget 例子')

        operatorLayout = QHBoxLayout()
        addBtn = QPushButton('添加节点')
        updateBtn = QPushButton('修改节点')
        deleteBtn = QPushButton('删除节点')

        operatorLayout.addWidget(addBtn)
        operatorLayout.addWidget(updateBtn)
        operatorLayout.addWidget(deleteBtn)

        addBtn.clicked.connect(self.addNode)
        updateBtn.clicked.connect(self.updateNode)
        deleteBtn.clicked.connect(self.deleteNode)

        self.tree = QTreeWidget()

        self.tree.setColumnCount(2)

        self.tree.setHeaderLabels(['Key','Value'])

        root  = QTreeWidgetItem(self.tree)
        root.setText(0,'root')
        root.setText(1, '0')
        #节点可编辑
        root.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

        child1 = QTreeWidgetItem(root)
        child1.setText(0,'child1')
        child1.setText(1,'1')

        child2 = QTreeWidgetItem(root)
        child2.setText(0,'child2')
        child2.setText(1,'2')

        child3 = QTreeWidgetItem(child2)
        child3.setText(0,'child3')
        child3.setText(1,'3')
        self.tree.clicked.connect(self.onTreeClicked)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(operatorLayout)
        mainLayout.addWidget(self.tree)
        self.setLayout(mainLayout)

    def onTreeClicked(self,index):
        item = self.tree.currentItem()
        print(index.row())
        print('key=%s,value=%s' % (item.text(0),item.text(1)))

    # 添加节点
    def addNode(self):
        print('添加节点')
        item = self.tree.currentItem()
        print(item)
        node = QTreeWidgetItem(item)
        node.setText(0,'新节点')
        node.setText(1,'新值')
        node.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

    def updateNode(self):
        print('修改节点')
        item = self.tree.currentItem()
        item.setText(0,'修改节点')
        item.setText(1, '值已经被修改')



    def deleteNode(self):
        print('删除节点')
        item = self.tree.currentItem()
        #根节点，根节点默认不显示，无此根节点删除出错
        root = self.tree.invisibleRootItem()
        for item in self.tree.selectedItems():
            #只要有一个不为空
            (item.parent() or root).removeChild(item)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = ModifyTree()
    tree.show()
    sys.exit(app.exec_())
