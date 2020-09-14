import sys

from PyQt5.QtWidgets import QApplication

import qtui.WindowMain as windowMain


class startApp():

    # 启动UI界面
    def startUi(self):
        app = QApplication(sys.argv)
        dispatch = windowMain.SignalEmit()
        sys.exit(app.exec_())

    # 初始化字典
    def initDict(self):
        # 扫描设备回调
        pass

if __name__ =='__main__':
    startApp = startApp()
    startApp.initDict()
    startApp.startUi()