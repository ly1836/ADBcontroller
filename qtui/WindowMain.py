from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QHBoxLayout, \
    QComboBox, QGridLayout, QTextEdit

from service.RecordClicks import RecordClicks
from service.ScanDeviceThread import ScanDeviceThread
from service.TranscribeThread import TranscribeThread

lineBreak = "\n"

class SignalEmit(QWidget):
    printLogSignal = pyqtSignal(str)
    printSignal = pyqtSignal(list)
    # 声明一个多重载版本的信号，包括了一个带int和str类型参数的信号，以及带str参数的信号
    previewSignal = pyqtSignal([int, str], [str])

    rc = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.creatContorls("控制：")
        self.creatResult("日志：")

        layout = QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        layout.addWidget(self.resultGroup)
        self.setLayout(layout)

        self.printLogSignal.connect(self.printLog)
        self.printSignal.connect(self.printPaper)
        self.previewSignal[str].connect(self.previewPaper)
        self.previewSignal[int, str].connect(self.previewPaperWithArgs)
        self.printButton.clicked.connect(self.emitPrintSignal)
        self.clearLogButton.clicked.connect(self.cleanLogSignal)
        self.scanDeviceButton.clicked.connect(self.scanDevicegSignal)
        self.setDeviceButton.clicked.connect(self.setDevicegSignal)
        self.transcribeButton.clicked.connect(self.transcribeSignal)
        self.playShellButton.clicked.connect(self.playShellSignal)

        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('ADB命令重放')
        self.show()

    def creatContorls(self, title):
        self.controlsGroup = QGroupBox(title)

        self.printButton = QPushButton("打印")
        self.clearLogButton = QPushButton("清除日志")
        self.scanDeviceButton = QPushButton("扫描设备")
        self.setDeviceButton = QPushButton("设置设备号")
        self.setDeviceButton.setEnabled(False)
        self.transcribeButton = QPushButton("录制脚本")
        self.transcribeButton.setEnabled(False)
        self.playShellButton = QPushButton("重放脚本")
        self.playShellButton.setEnabled(False)

        self.styleCombo = QComboBox(self)
        self.styleCombo.setEnabled(False)

        # numberLabel = QLabel("打印份数：")
        # pageLabel = QLabel("纸张类型：")

        # self.previewStatus = QCheckBox("全屏预览")

        # self.numberSpinBox = QSpinBox()
        # self.numberSpinBox.setRange(1, 100)

        controlsLayout = QGridLayout()
        # controlsLayout.addWidget(numberLabel, 0, 0)
        # controlsLayout.addWidget(self.numberSpinBox, 0, 1)
        # controlsLayout.addWidget(pageLabel, 0, 2)
        # controlsLayout.addWidget(self.printButton, 0, 4)
        # controlsLayout.addWidget(self.previewStatus, 3, 0)

        controlsLayout.addWidget(self.scanDeviceButton, 2, 1)
        controlsLayout.addWidget(self.styleCombo, 2, 2)
        controlsLayout.addWidget(self.setDeviceButton, 2, 3)
        controlsLayout.addWidget(self.transcribeButton, 3, 1)
        controlsLayout.addWidget(self.playShellButton, 3, 2)
        self.controlsGroup.setLayout(controlsLayout)

    # 初始化日志区
    def creatResult(self, title):
        self.resultGroup = QGroupBox(title)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        textFont = QFont("Microsoft YaHei")
        textFont.setPointSize(10)
        self.textEdit.setFont(textFont)

        layout = QGridLayout()

        layout.addWidget(self.textEdit, 1,1)
        layout.addWidget(self.clearLogButton, 2,1)
        self.resultGroup.setLayout(layout)

    def emitPreviewSignal(self):
        if self.previewStatus.isChecked() == True:
            self.previewSignal[int, str].emit(1080, " Full Screen")
        elif self.previewStatus.isChecked() == False:
            self.previewSignal[str].emit("Preview")

    # 清空日志区
    def cleanLogSignal(self):
        self.textEdit.clear()

    # 设置设备号
    def setDevicegSignal(self):
        index = self.styleCombo.currentIndex()
        text = self.styleCombo.currentText()
        self.rc.setDevice(index)
        self.textEdit.insertPlainText("当前设备选中为【%s】" % text + lineBreak)

    # 录制脚本
    def transcribeSignal(self):
        # self.rc.transcribe(self)
        self.rc = TranscribeThread(self.rc.device, self)
        self.rc.start()

    # 重放脚本
    def playShellSignal(self):
        self.rc.playShell(self)

    # 扫描设备
    def scanDevicegSignal(self):
        if(self.rc == None):
            self.rc = RecordClicks("127.0.0.1", 5037)
            #self.rc = ScanDeviceThread("127.0.0.1", 5037, self)
            #self.rc.startScan()

        device_list = self.rc.getDeviceList()

        if(device_list != None):
            self.textEdit.insertPlainText("扫描到[%s]个设备" % device_list.__len__() + lineBreak)
            for device in device_list:
                self.textEdit.insertPlainText("设备号:[%s]" % device.get_serial_no() + lineBreak)

        self.createCombo()
        self.styleCombo.setEnabled(True)
        self.setDeviceButton.setEnabled(True)
        self.transcribeButton.setEnabled(True)
        self.playShellButton.setEnabled(True)

    # 根据扫描到的设备列表生成下来框
    def createCombo(self):
        for idx, val in enumerate(self.rc.deviceList):
            self.styleCombo.addItem(val.get_serial_no(), idx)


    def emitPrintSignal(self):
        pList = []
        pList.append(self.numberSpinBox.value())
        pList.append(self.styleCombo.currentText())
        self.printSignal.emit(pList)

    def printPaper(self, list):
        self.textEdit.insertPlainText("Print: " + "份数：" + str(list[0]) + "  纸张：" + str(list[1]) + lineBreak)

    def previewPaperWithArgs(self, style, text):
        self.textEdit.insertPlainText(str(style) + text + lineBreak)

    def previewPaper(self, text):
        self.textEdit.insertPlainText(text + lineBreak)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.printLogSignal.emit("打印日志...." + lineBreak)

    def printLog(self, message):
        self.textEdit.insertPlainText(message + lineBreak)
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())
