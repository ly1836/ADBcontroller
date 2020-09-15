import configparser
import os



class Properties():
    cp = None

    def __init__(self):
        # 启动类所在路径，
        path = os.getcwd()
        self.cp = configparser.ConfigParser()
        self.cp.read(path + "/config/db.cfg")

    # 扫描设备回调类型
    def getTypeByScanDevice(self):
        section = self.cp.sections()[0]
        return int(self.cp.get(section, "scan_device"))
    # 截图成功回调类型
    def getTypeByScreencap(self):
        section = self.cp.sections()[0]
        return int(self.cp.get(section, "screencap"))

    # adb 点击事件X轴特征
    def getWide(self):
        section = self.cp.sections()[1]
        return str(self.cp.get(section, "wide"))

    # adb 点击事件Y轴特征
    def getHigh(self):
        section = self.cp.sections()[1]
        return str(self.cp.get(section, "high"))

    # adb 点击事件原点特征
    def getEmpty(self):
        section = self.cp.sections()[1]
        return str(self.cp.get(section, "empty"))

    # adb 截图上传间隔时间 单位：秒
    def getScreencapIntervalTime(self):
        section = self.cp.sections()[1]
        intervalTime = int(self.cp.get(section, "screencap_interval_time"))
        if intervalTime < 1:
            intervalTime = 1
        return intervalTime

    # 日志文件路径名称
    def getLogFilename(self):
        section = self.cp.sections()[2]
        return str(self.cp.get(section, "logFilename"))

    # 日志等级
    def getLogLevel(self):
        section = self.cp.sections()[2]
        return str(self.cp.get(section, "logLevel"))

    # 日志格式化
    def getLogFormat(self):
        section = self.cp.sections()[2]
        return str(self.cp.get(section, "logFormat"))

    # 监控区默认图片路径
    def getMonitorInitImage(self):
        section = self.cp.sections()[3]
        return str(self.cp.get(section, "monitor_init_image"))

    # 监控区图片路径
    def getMonitorImage(self):
        section = self.cp.sections()[3]
        return str(self.cp.get(section, "monitor_image"))