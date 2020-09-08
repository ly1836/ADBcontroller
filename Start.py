import sys

import qtui.WindowMain as windowMain

from PyQt5.QtWidgets import QApplication, QMainWindow

class startApp():

    # 启动UI界面
    def startUi(self):
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = windowMain.Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


if __name__ =='__main__':
    startApp = startApp()
    startApp.startUi()