import json

from config.Properties import Properties

dbPath = Properties().getDBPath()


# JSON处理工具类
class JSONUtil():

    # 保存事件到json文件
    def saveToLocal(self, data, fileName):
        # eventList = data.get("eventList")
        # newEventList = []
        # for d in eventList:
        #     newEventList.append(d)
        #
        # data.__setitem__("eventList", newEventList)

        with open(dbPath + fileName, 'w') as f:
            json.dump(data, f)

    # 读取json文件
    def load(self, fileName):
        with open(dbPath + fileName, 'r') as f:
            data = json.load(f)

        return data