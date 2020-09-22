import threading
from ppadb.client import Client as AdbClient

from config.Properties import Properties
from util.LogUtil import LogUtil
from util.ThreadUtil import ThreadUtil

lineBreak = "\n"
logging = LogUtil().getLogger()

## 扫描设备线程
class ScanDeviceThread(threading.Thread):
    deviceBO = None
    windowMain = None
    property = Properties()
    isRun = False

    def __init__(self, deviceBO, windowMain):
        super().__init__()
        self.deviceBO = deviceBO
        self.windowMain = windowMain

    def run(self):
        self.isRun = True
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
            self.isRun = False
            logging.error("扫描设备线程异常:", exc_info=True)
            self.windowMain.printLogSignal.emit("未扫描到已连接设备!\n%s" % str(ex))
            self.windowMain.scanDeviceButton.setEnabled(True)


    # 停止扫描线程
    def stop(self, windowMain):
        ThreadUtil(self).stopThread()
        windowMain.printLogSignal.emit("退出扫描设备线程:" + self.name + lineBreak)
        self.isRun = False

    # 获取屏幕分辨率
    def getResolutionRatio(self, windowMain):
        result = str(self.deviceBO.getDevice().shell("wm size"))
        split_ = result.replace("\r\n", "").split(": ")[1]
        screenRatio = split_.split("x")
        self.deviceBO.setScreenWidth(screenRatio[0])
        self.deviceBO.setScreenHigh(screenRatio[1])
        windowMain.printLogSignal.emit("获取设备分辨率成功：[%s]" % split_)
