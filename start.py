import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import ui.WindowMain as windowMain
from ui.ChooseConfigWindow import ChooseConfigWindow
from util.LogUtil import LogUtil

initHost = "127.0.0.1"
initPort = 5037
logging = LogUtil().getLogger()

class start():
    # 启动UI界面
    def startUi(self):
        global initHost, initPort
        app = QApplication(sys.argv)
        if (sys.argv.__len__() >= 3):
            initHost = sys.argv[1]
            initPort = int(sys.argv[2])

        print("当前设置的host=%s,port=%s" % (initHost, initPort))
        print("-----------------------------------------")
        mainWindow = windowMain.WindowMain(initHost, initPort)
        chooseConfig = ChooseConfigWindow(mainWindow)
        # chooseConfig.windowShow()

        mainWindow.chooseConfigButton.clicked.connect(chooseConfig.windowShow)

        mainWindow.setWindowIcon(QIcon("./resource/init/logo.png"))
        chooseConfig.setWindowIcon(QIcon("./resource/init/logo.png"))

        mainWindow.show()
        sys.exit(app.exec_())


if __name__ =='__main__':
    print("-----------------------------------------")
    print("按如下模板设置启动参数:")
    print("python start.py 127.0.0.1 5037")
    startApp = start()
    startApp.startUi()