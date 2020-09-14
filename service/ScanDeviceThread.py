import threading
import logging
from ppadb.client import Client as AdbClient
from service import logFilename, filemode, logFormat, logDatefmt

lineBreak = "\n"
logging.basicConfig(filename=logFilename, filemode=filemode, format=logFormat,
                    datefmt=logDatefmt, level=logging.DEBUG)

## 扫描设备线程
class ScanDeviceThread(threading.Thread):
    deviceBO = None
    windowMain = None

    # property = Properties()

    def __init__(self, deviceBO, windowMain):
        super().__init__()
        self.deviceBO = deviceBO
        self.windowMain = windowMain

    def run(self):
        self.windowMain.printLogSignal.emit("开启扫描设备线程....")
        try:
            type = self.property.getTypeByScanDevice()
            # 初始化连接
            client = AdbClient(host=self.deviceBO.getHost(), port=self.deviceBO.getPort())
            self.deviceBO.setClient(client)
            deviceList = client.devices()
            self.deviceBO.setDeviceList(deviceList)
            self.windowMain.callBackSignal.emit("扫描设备线程结束!", type)
        except Exception as ex:
            logging.error("扫描设备线程异常:", ex)
            self.windowMain.printLogSignal.emit("未扫描到已连接设备!")

    # 启动扫描线程
    def startScan(self):
        self.start()

    # 停止扫描线程
    def stopScan(self):
        self.stopFlag = False
        self.windowMain.printLogSignal.emit("退出扫描设备线程:" + self.name + lineBreak)
