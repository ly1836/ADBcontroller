import os
import json


class JSONUtil():

    # 保存事件到json文件
    def saveToLocal(self, data):
        # 剔除事件时间间隔小于100ms的记录点
        lastTime = None
        eventList = data.get("eventList")
        newEventList = []
        for d in eventList:
            if (lastTime != None):
                timeDiff = d["t"] - lastTime
                if (timeDiff > 300):
                    newEventList.append(d)
                    lastTime = d["t"]
            else:
                lastTime = d["t"]
                newEventList.append(d)

        data.__setitem__("eventList", newEventList)
        path = os.getcwd()
        with open(path + '/db/data.json', 'w') as f:
            json.dump(data, f)
