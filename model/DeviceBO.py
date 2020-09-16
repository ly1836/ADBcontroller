

class DeviceBO():
    # 主机IP
    host = None
    # 端口
    port = None
    # 客户端对象
    client = None
    # 设备列表
    deviceList = None
    # 当前连接设备
    device = None

    # 屏幕分辨率宽
    screenWidth =None
    # 屏幕分辨率高
    screenHigh = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def setHost(self, host):
        self.host = host

    def getHost(self):
        return self.host

    def setPort(self, port):
        self.port = port

    def getPort(self):
        return self.port

    def setClient(self, client):
        self.client = client

    def getClient(self):
        return self.client

    def setDeviceList(self, deviceList):
        self.deviceList = deviceList

    def getDeviceList(self):
        return self.deviceList

    def setDevice(self, device):
        self.device = device

    def getDevice(self):
        return self.device

    def setScreenWidth(self, screenWidth):
        self.screenWidth = screenWidth

    def getScreenWidth(self):
        return self.screenWidth

    def setScreenHigh(self, screenHigh):
        self.screenHigh = screenHigh

    def getScreenHigh(self):
        return self.screenHigh