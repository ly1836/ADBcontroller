import os

from ppadb.client import Client as AdbClient
import time
import json
import threading


class RecordClicks(threading.Thread):
    wide = None
    high = None
    empty = None
    device = None
    host = None
    port = None
    data = {
        "eventList": [
        ],
        "author": "ly"
    }

    def run(self):
        print("开始线程：" + self.name)

        # 初始化连接
        client = AdbClient(host=self.host, port=self.port)
        # "127.0.0.1:62001"
        deviceList = self.getDeviceList(client)

        self.device = deviceList[0]
        self.device.shell('getevent', handler=self.get_click_handler)
        time.sleep(9999999999999)
        print("退出线程：" + self.name)

    def __init__(self, host, port):
        # 宽
        super().__init__()
        self.wide = "0003 0035 "
        # 高
        self.high = "0003 0036 "
        self.empty = "00000000"
        self.host = host
        self.port = port

    # 获取设备列表
    def getDeviceList(self, client):
        # 获取设备列表
        devices = client.devices()
        print("获取设备列表：")
        print("===================")
        for dev in devices:
            # 获取设备序列号
            serialNo = dev.get_serial_no()
            print(serialNo)
        print("===================")
        return devices

    # 回调事件
    def get_click_handler(self, connection):
        print("监听屏幕点击事件中...")
        while True:
            data = connection.read(1024)
            str = data.decode('utf-8')
            splitlines = str.splitlines()
            event = {"time": int(time.time())}
            for split in splitlines:

                if (self.wide in split) and (self.empty not in split):
                    wide_ = split.split(self.wide)[1]
                    # 宽转10进制数字
                    wide_16 = int(wide_, 16)
                    print(r"点击的x轴：[%s]" % wide_16)
                    event["x"] = wide_16
                if ((self.high in split) and (self.empty not in split)):
                    high_ = split.split(self.high)[1]
                    # 高转10进制数字
                    high_16 = int(high_, 16)
                    print(r"点击的y轴：[%s]" % high_16)
                    event["y"] = high_16

            if ((event.get("x") is not None) and (event.get("y") is not None)):
                eventList = self.data.get("eventList")
                if (eventList.__len__() > 0):
                    eventList.append(event)
                else:
                    eventList = []
                    eventList.append(event)
                self.data["eventList"] = eventList
                # 保存事件到json文件
                self.save()

    # 保存事件到json文件
    def save(self):
        path = os.getcwd()
        print(path)
        with open(path + '/db/data.json', 'w') as f:
            json.dump(self.data, f)

# if __name__ == "__main__":
#     # adb get-serialno
#     rc = RecordClicks("127.0.0.1", 5037)
