import sys

from PyQt5.QtWidgets import QApplication

import qtui.WindowMain as windowMain

initHost = "127.0.0.1"
initPort = 5037

class startApp():


    # 启动UI界面
    def startUi(self, initHost=None, initPort=None):
        app = QApplication(sys.argv)
        if (sys.argv.__len__() < 3):
            print("当前设置的host=%s,port=%s" % (initHost, initPort))
            print("-----------------------------------------")
            dispatch = windowMain.WindowMain(initHost, initPort)
        else:
            initHost = sys.argv[1]
            initPort = int(sys.argv[2])
            print("当前设置的host=%s,port=%s" % (initHost, initPort))
            print("-----------------------------------------")
            dispatch = windowMain.WindowMain(initHost, initPort)
        sys.exit(app.exec_())


if __name__ =='__main__':
    print("-----------------------------------------")
    print("按如下模板设置启动参数:")
    print("python start.py 127.0.0.1 5037")

    startApp = startApp()
    startApp.startUi(initHost, initPort)