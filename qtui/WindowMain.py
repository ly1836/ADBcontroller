import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QHBoxLayout, \
    QComboBox, QGridLayout, QTextEdit

from model.DeviceBO import DeviceBO
from service.ScanDeviceThread import ScanDeviceThread
from service.TranscribeThread import TranscribeThread
import logging

from util.ThreadUtil import ThreadUtil

lineBreak = "\n"
logDatePrefix = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(filename="log.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)

class SignalEmit(QWidget):
    printLogSignal = pyqtSignal(str)
    callBackSignal = pyqtSignal(str, int)
    # 声明一个多重载版本的信号，包括了一个带int和str类型参数的信号，以及带str参数的信号
    previewSignal = pyqtSignal([int, str], [str])

    # 当前连接设备
    scanDevice = None
    # 录制脚本
    transcribe = None

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
        self.callBackSignal.connect(self.callBack)
        self.previewSignal[str].connect(self.previewPaper)
        self.previewSignal[int, str].connect(self.previewPaperWithArgs)
        self.printButton.clicked.connect(self.emitPrintSignal)
        self.clearLogButton.clicked.connect(self.cleanLogSignal)
        self.scanDeviceButton.clicked.connect(self.scanDevicegSignal)
        self.setDeviceButton.clicked.connect(self.setDevicegSignal)
        self.transcribeButton.clicked.connect(self.transcribeSignal)
        self.stopTranscribeButton.clicked.connect(self.stopTranscribeSignal)
        self.playShellButton.clicked.connect(self.playShellSignal)

        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('ADB命令重放')
        self.show()

    def creatContorls(self, title):
        self.controlsGroup = QGroupBox(title)

        self.printButton = QPushButton("打印")
        self.clearLogButton = QPushButton("清除日志")
        self.scanDeviceButton = QPushButton("扫描设备")
        self.setDeviceButton = QPushButton("选中当前设备号")
        self.setDeviceButton.setEnabled(False)

        self.transcribeButton = QPushButton("录制脚本")
        self.transcribeButton.setEnabled(False)
        self.stopTranscribeButton = QPushButton("停止录制")
        self.stopTranscribeButton.setEnabled(False)
        self.playShellButton = QPushButton("重放脚本")
        self.playShellButton.setEnabled(False)

        self.styleCombo = QComboBox(self)
        self.styleCombo.setEnabled(False)
        self.styleCombo.currentTextChanged.connect(self.comboBoxChanged)

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
        controlsLayout.addWidget(self.stopTranscribeButton, 3, 2)
        controlsLayout.addWidget(self.playShellButton, 3, 3)
        self.controlsGroup.setLayout(controlsLayout)

    # 初始化日志区
    def creatResult(self, title):
        self.resultGroup = QGroupBox(title)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
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

    # 设备列表下拉框切换选项触发事件
    def comboBoxChanged(self):
        index = self.styleCombo.currentIndex()
        text = self.styleCombo.currentText()
        self.scanDevice.deviceBO.setDevice(self.scanDevice.deviceBO.getDeviceList()[index])
        self.printLog("当前设备选中为【%s】" % text)

    # 选中设备号
    def setDevicegSignal(self):
        index = self.styleCombo.currentIndex()
        text = self.styleCombo.currentText()
        self.scanDevice.deviceBO.setDevice(self.scanDevice.deviceBO.getDeviceList()[index])
        self.printLog("当前设备选中为【%s】" % text)

    # 录制脚本
    def transcribeSignal(self):
        self.transcribe = TranscribeThread(self.scanDevice.deviceBO.getDevice(), self)
        self.transcribe.start()

        self.scanDeviceButton.setEnabled(False)
        self.styleCombo.setEnabled(False)
        self.setDeviceButton.setEnabled(False)
        self.transcribeButton.setEnabled(False)
        self.stopTranscribeButton.setEnabled(True)
        self.playShellButton.setEnabled(False)

    # 停止录制脚本
    def stopTranscribeSignal(self):
        self.transcribe.stop(self)

        self.scanDeviceButton.setEnabled(True)
        self.styleCombo.setEnabled(True)
        self.setDeviceButton.setEnabled(True)
        self.transcribeButton.setEnabled(True)
        self.stopTranscribeButton.setEnabled(False)
        self.playShellButton.setEnabled(True)


    # 重放脚本
    def playShellSignal(self):
        self.transcribe.playShell(self)

    # 扫描设备
    def scanDevicegSignal(self):
        self.scanDevice = DeviceBO("127.0.0.1", 5037)
        self.scanDevice = ScanDeviceThread(self.scanDevice, self)
        self.scanDevice.startScan()

    # 根据扫描到的设备列表生成下拉框
    def createCombo(self):
        for idx, val in enumerate(self.scanDevice.deviceBO.getDeviceList()):
            self.styleCombo.addItem(val.get_serial_no(), idx)

    def emitPrintSignal(self):
        pList = []
        pList.append(self.numberSpinBox.value())
        pList.append(self.styleCombo.currentText())
        self.printSignal.emit(pList)

    def previewPaperWithArgs(self, style, text):
        self.textEdit.insertPlainText(str(style) + text + lineBreak)

    def previewPaper(self, text):
        self.textEdit.insertPlainText(text + lineBreak)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.printLog("打印日志....")

    # 输出日志
    def printLog(self, message):
        nowTime = time.strftime(logDatePrefix, time.localtime())
        self.textEdit.insertPlainText(nowTime + "：" + message + lineBreak)
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())

    # type -->1:扫描设备回调
    def callBack(self, message, type):
        if(type == 1):
            try:
                self.printLog(message)
                device_list = self.scanDevice.deviceBO.getDeviceList()

                if (device_list != None):
                    self.printLog("扫描到[%s]个设备" % device_list.__len__())
                    for device in device_list:
                        self.printLog("设备号:[%s]" % device.get_serial_no())

                self.createCombo()
                self.styleCombo.setEnabled(True)
                self.setDeviceButton.setEnabled(True)
                self.transcribeButton.setEnabled(True)
                self.stopTranscribeButton.setEnabled(True)
                self.playShellButton.setEnabled(True)
            except Exception as ex:
                logging.error(ex)


