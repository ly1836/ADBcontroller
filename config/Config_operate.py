import configparser
import os

path = os.getcwd()
cp = configparser.ConfigParser()
cp.read(path + "/config/db.cfg")

class Properties():

    def getTypeByScanDevice(self):
        section = cp.sections()[0]
        return int(cp.get(section, "scan_device"))

    def getWide(self):
        section = cp.sections()[1]
        return str(cp.get(section, "wide"))

    def getHigh(self):
        section = cp.sections()[1]
        return str(cp.get(section, "high"))

    def getEmpty(self):
        section = cp.sections()[1]
        return str(cp.get(section, "empty"))
