import os

from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMessageBox, QTreeWidget, QTreeWidgetItem, QMainWindow, QAction, QInputDialog, QLineEdit, \
    QAbstractItemView

from config.Properties import Properties
from util.LogUtil import LogUtil

showMessage = QMessageBox.question

lineBreak = "\n"
logDatePrefix = "%Y-%m-%d %H:%M:%S"
logging = LogUtil().getLogger()
treeFolderImage = Properties().getTreeFolderImage()
dbPath = Properties().getDBPath()


# 选择配置窗口
class ChooseConfigWindow(QMainWindow):
    windowMain = None

    def __init__(self, windowMain, parent=None):
        super(ChooseConfigWindow, self).__init__(parent)
        self.windowMain = windowMain
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('选择功能')
        self.resize(600, 600)

        # 添加收藏夹，根节点的父是 QTreeWidget对象
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        # 是表，则有表头
        self.tree.setHeaderLabels(['功能列表'])

        self.tree.clicked.connect(self.onClicked)
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.f_item = self.tree.headerItem()

        # 添加一个初始文件夹
        # child = QTreeWidgetItem(self.tree)
        # child.setText(0, '目录')
        # child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        # child.setIcon(0, QIcon(treeFolderImage))
        self.initDataItem()

        # 以下是窗口的设置
        self.setCentralWidget(self.tree)

        # addAction = QAction("添加新子节点", self)
        # addAction.triggered.connect(self.addItem)
        addAction = QAction("添加目录", self)
        addAction.triggered.connect(self.addFolder)
        deleteAction = QAction("删除", self)
        deleteAction.triggered.connect(self.deleteItem)
        editAction = QAction("修改", self)
        editAction.triggered.connect(self.editItem)

        toolbar = self.addToolBar("")
        # toolbar.addAction(addAction)
        toolbar.addAction(addAction)
        toolbar.addAction(deleteAction)
        toolbar.addAction(editAction)
        self.show()

    # 初始化数据节点
    def initDataItem(self):
        files = os.listdir(dbPath)
        for file in files:
            if os.path.isdir(dbPath + file):
                print("文件夹：" + file)
                self.addFolderByName(file)
            else:
                print("文件：" + file)

    # 添加树控件子节点
    def addItem(self, name):
        currNode = self.tree.currentItem()
        if currNode is not None:
            addChild = QTreeWidgetItem()
            addChild.setText(0, name)
            currNode.addChild(addChild)
        else:
            self.addFolder()

    # 添加文件夹
    def addFolder(self):
        value, ok = QInputDialog.getText(self, "名称", "请输入名称:", QLineEdit.Normal, "")
        if ok:
            value = value.replace(" ", "")
            child = QTreeWidgetItem(self.tree)
            child.setText(0, value)
            child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            child.setIcon(0, QIcon(treeFolderImage))

            filePath = dbPath + value
            folder = os.path.exists(filePath)
            if not folder:
                os.makedirs(filePath)

    # 添加文件夹
    def addFolderByName(self, folderName):
        child = QTreeWidgetItem(self.tree)
        child.setText(0, folderName)
        child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        child.setIcon(0, QIcon(treeFolderImage))

    # 删除控件树子节点/根节点
    def deleteItem(self):
        try:
            # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
            currNode = self.tree.currentItem()
            if currNode is not None:
                parentNode = currNode.parent()
                if parentNode is not None:
                    reply = showMessage(self, '警告', "是否删除文件-%s?" % (currNode.text(0)),
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        parentNode.removeChild(currNode)

                        self.removeFile(currNode.text(0))
                else:
                    reply = showMessage(self, '警告', "是否删除文件夹及下面所有文件-%s?" % (currNode.text(0)),
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        rootIndex = self.tree.indexOfTopLevelItem(currNode)
                        self.tree.takeTopLevelItem(rootIndex)

                        self.removeFile(currNode.text(0))

            else:
                QMessageBox.information(self, '消息', '未选择节点')
        except Exception:
            logging.error("删除节点异常:", exc_info=True)

    # 删除文件
    def removeFile(self, file):
        try:
            filePath = dbPath + file
            folder = os.path.exists(filePath)
            if folder:
                os.remove(filePath)
        except Exception:
            logging.error("删除文件异常:", exc_info=True)

    # 修改节点
    def editItem(self):
        try:
            currNode = self.tree.currentItem()
            if currNode is not None:
                value, ok = QInputDialog.getText(self, "名称", "请输入新名称:", QLineEdit.Normal, "")
                if ok:
                    currNode.setText(0, value)
            else:
                QMessageBox.information(self, '消息', '未选择节点')
        except Exception:
            logging.error("修改节点异常:", exc_info=True)

    # 树节点点击事件
    def onClicked(self):
        # 将之前选中的子项目背景色还原
        self.f_item.setBackground(0, QColor(255, 255, 255))
        # 获取当前选中项
        item = self.tree.currentItem()
        # 设置当前选择项背景
        item.setBackground(0, QColor('#AFEEEE'))
        # 更新前选中项
        self.f_item = item

    # 窗口显示
    def windowShow(self):
        if not self.isVisible():
            self.show()

    # def onClicked(self):
    #     item = self.tree.currentItem()
    #     print('Key=%s,value=%s' % (item.text(0), item.text(1)))
