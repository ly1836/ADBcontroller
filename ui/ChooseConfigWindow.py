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
treeFileImage = Properties().getTreeFileImage()
dbPath = Properties().getDBPath()


# 选择配置窗口
class ChooseConfigWindow(QMainWindow):
    windowMain = None

    twoClick = 1

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

        # 以下是窗口的设置
        self.setCentralWidget(self.tree)

        # 递归建树
        self.initDataItem(dbPath, self.tree)
        # 取消默认选中
        self.tree.setCurrentItem(None)

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

    # 初始化数据节点
    def initDataItem(self, upperPath, item = None):
        files = os.listdir(upperPath)
        fileCount = files.__len__()
        for index in range(fileCount):
            file = files[index]
            currentpath = upperPath + "/" + file
            if os.path.isdir(currentpath):
                print("文件夹：" + file)

                child = self.addFolderByName(file, item)
                self.initDataItem(currentpath, child)
            else:
                print("文件：" + file)
                self.addItem(item, file)

    # 添加树控件子节点
    def addItem(self, currentNode, name):
        # 不是json文件不加载
        if(name.find(".json") == -1):
            return

        name = name.replace(".json", "")
        if currentNode is not None:
            addChild = QTreeWidgetItem(currentNode)
            addChild.setText(0, name)
            addChild.setIcon(0, QIcon(treeFileImage))
            # currNode.addChild(addChild)
        else:
            self.addFolder()

    # 添加文件夹
    def addFolder(self):
        try:
            value, ok = QInputDialog.getText(self, "名称", "请输入名称:", QLineEdit.Normal, "")
            if ok:
                value = value.replace(" ", "")
                item = self.tree.currentItem()
                if item is None:
                    item = self.tree

                fullPath = dbPath + self.getFullPathByNode(item)
                folder = os.path.exists(fullPath)
                if folder:
                    child = QTreeWidgetItem(item)
                    child.setText(0, value)
                    child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    child.setIcon(0, QIcon(treeFolderImage))

                    fullPath = dbPath + self.getFullPathByNode(item) + "/" + value
                    os.makedirs(fullPath)
                else:
                    QMessageBox.information(self, '消息', "不能在文件下新建文件夹！")
        except Exception as e:
            logging.error("添加节点异常:", exc_info=True)
            QMessageBox.information(self, '消息', str(e))

    # 添加文件夹
    def addFolderByName(self, folderName, currentNode):
        child = QTreeWidgetItem(currentNode)
        child.setText(0, folderName)
        child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        child.setIcon(0, QIcon(treeFolderImage))
        return child

    # 删除控件树子节点/根节点
    def deleteItem(self):
        try:
            # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
            currNode = self.tree.currentItem()
            if currNode is not None:
                fullPath = dbPath + self.getFullPathByNode(currNode)
                folder = os.path.exists(fullPath)
                if not folder:
                    reply = showMessage(self, '警告', "是否删除文件-%s?" % (currNode.text(0)),
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        fullPath += ".json"
                        flag = self.removeFile(fullPath)
                        if flag:
                            # parentNode.removeChild(currNode)
                            parent = self.tree.currentItem().parent()
                            if parent is None:
                                rootIndex = self.tree.indexOfTopLevelItem(currNode)
                                self.tree.takeTopLevelItem(rootIndex)
                            else:
                                parent.removeChild(self.tree.currentItem())
                else:
                    reply = showMessage(self, '警告', "是否删除文件夹及下面所有文件-%s?" % (currNode.text(0)),
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        flag = self.removeFile(fullPath)
                        if flag:
                            parent = self.tree.currentItem().parent()
                            if parent is None:
                                rootIndex = self.tree.indexOfTopLevelItem(currNode)
                                self.tree.takeTopLevelItem(rootIndex)
                            else:
                                parent.removeChild(self.tree.currentItem())

            else:
                QMessageBox.information(self, '消息', '未选择节点')
        except Exception as e:
            logging.error("删除节点异常:", exc_info=True)
            QMessageBox.information(self, '消息', e.args[1])

    # 删除文件
    def removeFile(self, filePath):
        try:
            if os.path.isdir(filePath):
                os.removedirs(filePath)
                return True
            elif os.path.isfile(filePath):
                os.remove(filePath)
                return True
        except Exception as e:
            logging.error("删除文件异常:", exc_info=True)
            QMessageBox.information(self, '消息', e.args[1])

        return False

    # 修改节点
    def editItem(self):
        try:
            currNode = self.tree.currentItem()
            if currNode is not None:
                value, ok = QInputDialog.getText(self, "名称", "请输入新名称:", QLineEdit.Normal, "")
                if ok:
                    oldFileName = dbPath + self.getFullPathByNode(currNode)
                    newFilePath = oldFileName[0: oldFileName.rfind("/")]
                    os.rename(oldFileName, newFilePath)
                    currNode.setText(0, value)
            else:
                QMessageBox.information(self, '消息', '未选择节点')
        except Exception as e:
            logging.error("修改节点异常:", exc_info=True)
            QMessageBox.information(self, '消息', e.args[1])

    # 树节点点击事件
    def onClicked(self):
        try:
            # 同一节点点击两次则取消选中
            if(self.f_item == self.tree.currentItem() and self.twoClick == 1):
                self.tree.setCurrentItem(None)
                # 将之前选中的子项目背景色还原
                self.f_item.setBackground(0, QColor(255, 255, 255))
                self.twoClick = 2
            else:
                # 将之前选中的子项目背景色还原
                self.f_item.setBackground(0, QColor(255, 255, 255))
                # 获取当前选中项
                item = self.tree.currentItem()
                if item is not None:
                    # 设置当前选择项背景
                    item.setBackground(0, QColor('#AFEEEE'))
                    # 更新前选中项
                    self.f_item = item
                    self.twoClick = 1
        except Exception as e:
            logging.error("获取控件全路径异常:", exc_info=True)
            QMessageBox.information(self, '消息', str(e))

    # 窗口显示
    def windowShow(self):
        if not self.isVisible():
            self.show()

    # 获取指定节点全路径
    def getFullPathByNode(self, item):
        try:
            # 顶层节点
            if(item == self.tree):
                return "/"
            else:
                currentPath = item.text(0)

            parent = item.parent()
            if parent != None:
                return self.getFullPathByNode(parent) + "/" + currentPath
            else:
                return "/" + currentPath
        except Exception as ex:
            logging.error("获取控件全路径异常:", exc_info=True)
