import sys

from PyQt5.QtWidgets import QApplication

import qtui.WindowMain as windowMain


class startApp():

    # 启动UI界面
    def startUi(self):
        app = QApplication(sys.argv)
        dispatch = windowMain.SignalEmit()
        sys.exit(app.exec_())


if __name__ =='__main__':
    startApp = startApp()
    startApp.startUi()