import threading
import time

import asyncio
import aiofiles

from config.Properties import Properties
from util.LogUtil import LogUtil
from util.ThreadUtil import ThreadUtil

lineBreak = "\n"
logging = LogUtil().getLogger()
type = Properties().getTypeByScreencap()
intervalTime = Properties().getScreencapIntervalTime()


## 获取设备画面线程
class ScreencapThread(threading.Thread):
    device = None
    windowMain = None
    property = Properties()

    def __init__(self, device, windowMain):
        super().__init__()
        self.device = device
        self.windowMain = windowMain

    def run(self):
        self.windowMain.printLogSignal.emit("开启获取设备画面线程....")
        asyncio.run(self.screencapPush())

    # 每隔指定时间截图并上传
    async def screencapPush(self):
        while True:
            result = self.device.screencap()
            async with aiofiles.open(f"./resource/replay/adbScreencap.png", "wb") as fp:
                await fp.write(result)

            self.windowMain.callBackSignal.emit("截图上传成功!", type)
            # 时间间隔
            time.sleep(intervalTime)

    def stop(self, windowMain):
        ThreadUtil(self).stopThread()
        windowMain.printLogSignal.emit("结束获取设备画面监听线程:" + self.name)