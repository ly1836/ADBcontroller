import threading
import time

from config.Properties import Properties
from util.JSONUtil import JSONUtil
from util.LogUtil import LogUtil
from util.ThreadUtil import ThreadUtil

lineBreak = "\n"
logging = LogUtil().getLogger()
type = Properties().getTypeByPlayOver()

## 重放adb命令线程
class PlayShellThread(threading.Thread):
    windowMain = None
    device = None
    isRun = False

    def __init__(self, device, windowMain):
        super().__init__()
        self.device = device
        self.windowMain = windowMain

    def run(self):
        self.isRun = True
        self.windowMain.printLogSignal.emit("开启ADB命令重放线程:" + self.name)
        data = JSONUtil().load("data.json")
        if data != None:
            eventList = data.get("eventList")
            if eventList != None:
                for event in eventList:
                    it = int(event["it"])
                    # 在原始时间间隔上加300毫秒
                    time.sleep((it / 1000) + 300)
                    self.device.shell('input tap %s %s' % (event['x'], event['y']))

                self.windowMain.callBackSignal.emit("重放ADB命令结束!", type)
            else:
                self.windowMain.printLogSignal.emit("读取脚本数据失败:" + self.name)
        else:
            self.windowMain.printLogSignal.emit("读取脚本数据失败:" + self.name)


    def stop(self, windowMain):
        ThreadUtil(self).stopThread()
        windowMain.printLogSignal.emit("结束重放ADB命令线程:" + self.name)
        self.isRun = False