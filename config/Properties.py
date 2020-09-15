import configparser
import os



class Properties():
    cp = None

    def __init__(self):
        # 启动类所在路径，
        path = os.getcwd()
        self.cp = configparser.ConfigParser()
        self.cp.read(path + "/config/db.cfg")

    def getTypeByScanDevice(self):
        section = self.cp.sections()[0]
        return int(self.cp.get(section, "scan_device"))

    def getWide(self):
        section = self.cp.sections()[1]
        return str(self.cp.get(section, "wide"))

    def getHigh(self):
        section = self.cp.sections()[1]
        return str(self.cp.get(section, "high"))

    def getEmpty(self):
        section = self.cp.sections()[1]
        return str(self.cp.get(section, "empty"))

    def getLogFilename(self):
        section = self.cp.sections()[2]
        return str(self.cp.get(section, "logFilename"))

    def getLogLevel(self):
        section = self.cp.sections()[2]
        return str(self.cp.get(section, "logLevel"))

    def getLogFormat(self):
        section = self.cp.sections()[2]
        return str(self.cp.get(section, "logFormat"))

    def getMonitorInitImage(self):
        section = self.cp.sections()[3]
        return str(self.cp.get(section, "monitor_init_image"))