import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

class AppiumTest():
    desir_caps = {}

    def __init__(self, platformName, platformVesion, deviceName, appPackage, appActivity):
        # 设备的系统, 是安卓还是iOS
        self.desir_caps['platformName'] = platformName
        # 设备的版本号
        self.desir_caps['platformVesion'] = platformVesion
        # 设备的名称-adb devices
        self.desir_caps['deviceName'] = deviceName
        # app的包名, 通过aapt dump badging c:\\..\.apk
        self.desir_caps['appPackage'] = appPackage
        # app对应的Activity名
        self.desir_caps['appActivity'] = appActivity

    # 获取驱动
    def getDriver(self):
        return webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desir_caps)



if __name__ =='__main__':
    # 调用方法
    # com.android.systemui/.recents.RecentsActivity
    # com.pscrow.retail.pos.debug / com.pscrow.retail.pos.ui.mian.LaunchActivity
    driver = AppiumTest('Android', '6.0', 'sdk_phone_armv7', 'com.pscrow.retail.pos.debug',
                        'com.pscrow.retail.pos.ui.mian.LaunchActivity').getDriver()

    TouchAction(driver).tap(x=330, y=324).perform()
    time.sleep(3)
    TouchAction(driver).tap(x=637, y=497).perform()
    time.sleep(3)
    TouchAction(driver).tap(x=217, y=516).perform()
    time.sleep(3)
    TouchAction(driver).tap(x=758, y=148).perform()
    time.sleep(3)
    TouchAction(driver).tap(x=864, y=382).perform()
    time.sleep(3)
    TouchAction(driver).tap(x=541, y=363).perform()

    driver.close()


