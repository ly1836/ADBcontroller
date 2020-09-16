import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QHBoxLayout, \
    QComboBox, QGridLayout, QTextEdit, QVBoxLayout, QLabel, QMessageBox
import asyncio

from config.Properties import Properties
from model.DeviceBO import DeviceBO
from service.PlayShellThread import PlayShellThread
from service.ScanDeviceThread import ScanDeviceThread
from service.ScreencapThread import ScreencapThread
from service.TranscribeThread import TranscribeThread
from util.LogUtil import LogUtil

showMessage = QMessageBox.question

lineBreak = "\n"
logDatePrefix = "%Y-%m-%d %H:%M:%S"
logging = LogUtil().getLogger()
monitorImage = Properties().getMonitorImage()


class WindowMain(QWidget):
    printLogSignal = pyqtSignal(str)
    callBackSignal = pyqtSignal(str, int)
    # 声明一个多重载版本的信号，包括了一个带int和str类型参数的信号，以及带str参数的信号
    previewSignal = pyqtSignal([int, str], [str])

    # 当前连接设备线程
    scanDevice = None
    # 录制脚本线程
    transcribe = None
    # 录制画面线程
    screencap = None
    # 重放命令线程
    playShell = None

    # adb 连接的host
    host = None
    # adb 连接的port
    port = None

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.initUI()

    def initUI(self):
        self.creatMonitor("画面监控：")
        self.creatContorls("控制：")
        self.creatResult("日志：")

        layout = QGridLayout()
        # 6个参数表示控件名，行，列，占用行数，占用列数，对齐方式
        layout.addWidget(self.monitorGroup,1,1,2,1)
        layout.addWidget(self.controlsGroup,1,2)
        layout.addWidget(self.resultGroup,2,2)
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
        self.screencapButton.clicked.connect(self.screencapSignal)
        self.playShellButton.clicked.connect(self.playShellSignal)
        self.stopPlayShellButton.clicked.connect(self.stopPlayShellSignal)

        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('ADB Control')

    # 控制按钮区
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
        self.screencapButton = QPushButton("连接屏幕")
        self.screencapButton.setEnabled(False)

        self.playShellButton = QPushButton("重放命令")
        self.playShellButton.setEnabled(False)
        self.stopPlayShellButton = QPushButton("停止重放")
        self.stopPlayShellButton.setEnabled(False)

        self.styleCombo = QComboBox(self)
        self.styleCombo.setEnabled(False)
        self.styleCombo.currentTextChanged.connect(self.comboBoxChanged)

        self.separateLabel = QLabel("")

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
        controlsLayout.addWidget(self.screencapButton, 3, 3)
        controlsLayout.addWidget(self.separateLabel, 4, 1, 1, 3)
        controlsLayout.addWidget(self.playShellButton, 5, 1)
        controlsLayout.addWidget(self.stopPlayShellButton, 5, 2)
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

    # 初始化监控区
    def creatMonitor(self, title):
        self.monitorGroup = QGroupBox(title)
        imagePath = Properties().getMonitorInitImage()
        self.pix = QPixmap(imagePath)
        self.pix.scaled(QSize(540, 540), aspectRatioMode = Qt.IgnoreAspectRatio)
        self.monitorLabel = QLabel()
        self.monitorLabel.setPixmap(self.pix)
        self.monitorLabel.setStyleSheet("border: 1px solid black")
        self.monitorLabel.setScaledContents(True)

        self.monitorLayout = QGridLayout()
        self.monitorLayout.addWidget(self.monitorLabel)

        self.monitorGroup.setLayout(self.monitorLayout)

    # 重绘监控区图片
    def redraw(self, imagePath):
        self.monitorLayout.removeWidget(self.monitorLabel)

        self.pix = QPixmap(imagePath)
        self.pix = self.pix.scaled(QSize(960, 540), QtCore.Qt.KeepAspectRatio)
        self.monitorLabel = QLabel()
        self.monitorLabel.setPixmap(self.pix)
        self.monitorLabel.setStyleSheet("border: 1px solid black")
        self.monitorLabel.setScaledContents(True)

        self.monitorLayout.addWidget(self.monitorLabel)

    # 扫描设备
    def scanDevicegSignal(self):
        self.scanDevice = DeviceBO(self.host, self.port)
        self.scanDevice = ScanDeviceThread(self.scanDevice, self)
        self.scanDevice.setDaemon(True)
        self.scanDevice.start()

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
        self.transcribe.setDaemon(True)
        self.transcribe.start()

        # 异步截图并上传
        self.screencap = ScreencapThread(self.scanDevice.deviceBO.getDevice(), self)
        self.screencap.setDaemon(True)
        self.screencap.start()

        self.scanDeviceButton.setEnabled(False)
        self.styleCombo.setEnabled(False)
        self.setDeviceButton.setEnabled(False)
        self.transcribeButton.setEnabled(False)
        self.stopTranscribeButton.setEnabled(True)
        self.playShellButton.setEnabled(False)

    # 停止录制脚本
    def stopTranscribeSignal(self):
        if(self.transcribe != None and self.transcribe.isRun):
            self.transcribe.stop(self)
        if(self.screencap != None and self.screencap.isRun):
            self.screencap.stop(self)

        self.scanDeviceButton.setEnabled(True)
        self.styleCombo.setEnabled(True)
        self.setDeviceButton.setEnabled(True)
        self.transcribeButton.setEnabled(True)
        self.stopTranscribeButton.setEnabled(False)
        self.playShellButton.setEnabled(True)

    # 连接屏幕
    def screencapSignal(self):
        if (self.screencap != None and self.screencap.isRun):
            self.screencap.stop(self)
            self.screencapButton.setText("连接屏幕")
        else:
            self.screencapButton.setText("断开连接")
            # 异步截图并上传
            self.screencap = ScreencapThread(self.scanDevice.deviceBO.getDevice(), self)
            self.screencap.setDaemon(True)
            self.screencap.start()

    # 重放脚本
    def playShellSignal(self):
        self.playShell = PlayShellThread(self.scanDevice.deviceBO.getDevice(), self)
        self.playShell.setDaemon(True)
        self.playShell.start()

        # 异步截图并上传
        self.screencap = ScreencapThread(self.scanDevice.deviceBO.getDevice(), self)
        self.screencap.setDaemon(True)
        self.screencap.start()

        self.scanDeviceButton.setEnabled(False)
        self.styleCombo.setEnabled(False)
        self.setDeviceButton.setEnabled(False)
        self.transcribeButton.setEnabled(False)
        self.stopTranscribeButton.setEnabled(True)
        self.playShellButton.setEnabled(False)
        self.stopPlayShellButton.setEnabled(True)

    # 停止重放脚本
    def stopPlayShellSignal(self):
        if self.playShell != None and self.playShell.isRun:
            # 获取EventLoop:
            loop = asyncio.get_event_loop()
            # 执行coroutine
            loop.run_until_complete(self.screencap.delayedStop(self, 3))
            loop.close()

            self.scanDeviceButton.setEnabled(True)
            self.styleCombo.setEnabled(True)
            self.setDeviceButton.setEnabled(True)
            self.transcribeButton.setEnabled(True)
            self.stopTranscribeButton.setEnabled(True)
            self.playShellButton.setEnabled(True)
            self.stopPlayShellButton.setEnabled(False)


    # 根据扫描到的设备列表生成下拉框
    def createCombo(self):
        for idx, val in enumerate(self.scanDevice.deviceBO.getDeviceList()):
            self.styleCombo.addItem(val.get_serial_no(), idx)

    # 退出确认框
    def closeEvent(self, event):
        reply = showMessage(self, '警告', "系统将退出，是否确认?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.transcribe != None and self.transcribe.isRun:
                self.transcribe.stop(self)
            if self.screencap != None and self.screencap.isRun:
                self.screencap.stop(self)
            if self.scanDevice != None and self.scanDevice.isRun:
                self.scanDevice.stop(self)
            if self.playShell != None and self.playShell.isRun:
                self.playShell.stop(self)

            event.accept()
        else:
            event.ignore()

    # 输出日志
    def printLog(self, message):
        nowTime = time.strftime(logDatePrefix, time.localtime())
        self.textEdit.insertPlainText(nowTime + "：" + message + lineBreak)
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())

    # type -->
    # 1:扫描设备回调
    # 2:截图回调
    # 3:重放命令结束回调
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
                self.playShellButton.setEnabled(True)
                self.screencapButton.setEnabled(True)

                # 获取屏幕分辨率
                self.scanDevice.getResolutionRatio(self)
            except Exception as ex:
                logging.error("扫描设备回调异常:", exc_info=True)
        # 截图成功回调
        if (type == 2):
            try:
                logging.info("截图成功回调")
                self.redraw(monitorImage)
            except Exception as ex:
                logging.error("扫描设备回调异常:", exc_info=True)
        # 重放命令结束回调
        if (type == 3):
            try:
                logging.info("重放命令结束回调")
                asyncio.run(self.screencap.delayedStop(self, 3))
                self.playShell.stop(self)

                self.scanDeviceButton.setEnabled(True)
                self.styleCombo.setEnabled(True)
                self.setDeviceButton.setEnabled(True)
                self.transcribeButton.setEnabled(True)
                self.stopTranscribeButton.setEnabled(True)
                self.playShellButton.setEnabled(True)
            except Exception as ex:
                logging.error("重放ADB命令结束回调异常:", exc_info=True)

    #============================================================
    def emitPreviewSignal(self):
        if self.previewStatus.isChecked() == True:
            self.previewSignal[int, str].emit(1080, " Full Screen")
        elif self.previewStatus.isChecked() == False:
            self.previewSignal[str].emit("Preview")

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
    # ============================================================