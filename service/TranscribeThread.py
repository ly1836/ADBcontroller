import os

import time
import json
import threading

from config.Properties import Properties
from util.JSONUtil import JSONUtil
from util.LogUtil import LogUtil
from util.ThreadUtil import ThreadUtil

lineBreak = "\n"
logging = LogUtil().getLogger()

## 录制脚本线程
class TranscribeThread(threading.Thread):
    property = Properties()
    windowMain = None
    wide = property.getWide()
    high = property.getHigh()
    empty = property.getEmpty()
    device = None
    data = {
        "eventList": [
        ],
        "author": "ly"
    }

    def __init__(self, device, windowMain):
        super().__init__()
        self.device = device
        self.windowMain = windowMain

    def run(self):
        self.windowMain.printLogSignal.emit("开启点击事件监听线程:" + self.name)
        self.device.shell("getevent", handler=self.get_click_handler)

    def stop(self, windowMain):
        ThreadUtil(self).stopThread()
        windowMain.printLogSignal.emit("结束点击事件监听线程:" + self.name)

    # 重放脚本
    def playShell(self, windowMain):
        path = os.getcwd()
        with open(path + '/db/data.json', 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
            print(json_data)

        eventList = self.data.get("eventList")
        for event in eventList:
            time.sleep(3)
            self.device.shell('input tap %s %s' % (event['x'], event['y']))

    # 回调事件
    def get_click_handler(self, connection):
        self.windowMain.printLogSignal.emit("监听屏幕点击事件中....")

        while True:
            data = connection.read(1024)
            str = data.decode('utf-8')
            splitlines = str.splitlines()
            nowTime = lambda: int(round(time.time() * 1000))
            event = {"t": nowTime(), "it": 0}
            for split in splitlines:
                if (self.wide in split) and (self.empty not in split):
                    wide_ = split.split(self.wide)[1]
                    # 宽转10进制数字
                    wide_16 = int(wide_, 16)
                    self.windowMain.printLogSignal.emit("点击的x轴：[%s]" % wide_16)
                    event["x"] = wide_16
                if ((self.high in split) and (self.empty not in split)):
                    high_ = split.split(self.high)[1]
                    # 高转10进制数字
                    high_16 = int(high_, 16)
                    self.windowMain.printLogSignal.emit("点击的y轴：[%s]" % high_16)
                    event["y"] = high_16

            if ((event.get("x") is not None) and (event.get("y") is not None)):
                eventList = self.data.get("eventList")
                if (eventList.__len__() > 0):
                    # 获取最后一个点击事件
                    lastEvent = eventList[eventList.__len__() - 1]
                    now = lambda: int(round(time.time() * 1000))
                    # 最后一个点击事件的时间戳
                    lastTime = int(lastEvent.get("t"))
                    # 事件时间间隔小于200ms, 不记录
                    intervalTime = now() - lastTime
                    event["it"] = intervalTime
                    if (intervalTime < 200 and lastTime != 0):
                        logging.debug("事件时间间隔小于200ms x:[%s],y[%s],t[%s]" % (event.get("x"), event.get("y"), event.get("t")))
                        continue

                    eventList.append(event)
                else:
                    eventList = []
                    eventList.append(event)

                self.data["eventList"] = eventList

                # 保存事件到json文件
                jsonUtil = JSONUtil()
                jsonUtil.saveToLocal(self.data)
