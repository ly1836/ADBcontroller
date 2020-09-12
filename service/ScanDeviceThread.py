
import threading
import time
from ppadb.client import Client as AdbClient

lineBreak = "\n"

## 扫描设备线程
class ScanDeviceThread(threading.Thread):
    host = None
    port = None
    windowMain = None
    stopFlag = True
    client = None
    deviceList = None

    def __init__(self, host, port, windowMain):
        super().__init__()
        self.host = host
        self.port = port
        self.windowMain = windowMain

    def run(self):
        self.windowMain.printLogSignal.emit("开启扫描设备线程:" + self.name + lineBreak)
        # 初始化连接
        self.client = AdbClient(host=self.host, port=self.port)

    # 获取设备列表
    def getDeviceList(self):
        # 获取设备列表
        self.deviceList = self.client.devices()
        return self.deviceList

    # 启动扫描线程
    def startScan(self):
        thread = ScanDeviceThread(self.host, self.port, self.windowMain)
        thread.start()
        while self.stopFlag:
            time.sleep(5)
            if(self.client != None):
                break

    # 停止扫描线程
    def stopScan(self):
        self.stopFlag = False
        self.windowMain.printLogSignal.emit("退出扫描设备线程:" + self.name + lineBreak)

