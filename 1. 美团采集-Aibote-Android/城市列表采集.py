# 1. 导入 AndroidBotMain 类
import time

from a01startAPPandEnterToSearchBar import *
from a02PerShop import *
from toolkit.fileOperation import createFold
import os
from configTXT import TxtToDict


# 2. 自定义一个脚本类，继承 AndroidBotMain
class CustomAndroidScript(AndroidBotMain):
    # 3. 设置等待参数
    # 3.1 设置等待时间
    wait_timeout = 3
    # 3.2 设置重试间隔时长
    interval_timeout = 0.5

    # 4. 设置日志等级
    log_level = "INFO"  # "DEBUG"

    # 5. 设置方法超时是否抛出异常
    raise_err = False  # True

    # 6. 重写方法，编写脚本
    # 注意：此方法是脚本执行入口
    def script_main(self):
        main(self)


def slide(driver: AndroidBotMain, num, duration=0.2, waitTime=0.2):
    """
    正数为向下滑动\n
    对于小米10，num设定为800正好为一个屏幕
    :param driver:
    :param num:
    :param duration:
    :return:
    """
    windowSize = driver.get_window_size()
    driver.swipe(start_point=(windowSize['width'] / 2, windowSize['height'] / 2),
                 end_point=(windowSize['width'] / 2, windowSize['height'] / 2 - num), duration=duration)
    time.sleep(duration + waitTime)


def main(driver: CustomAndroidScript):
    """
    主函数
    :param driver:
    :return:
    """
    city = {}
    baseXPath = """com.sankuai.meituan/com.sankuai.meituan:id=citylist_textview[{}]"""
    count = 0
    while True:
        print("----------------")
        count += 1
        for i in range(16):
            temp = driver.get_element_text(baseXPath.format(i), wait_time=0.1)
            print(temp)
            city[str(temp)] = None
        slide(driver, 700)
        time.sleep(2)
        if count == 100:
            print("************** 100 **********************")



def init(driver: CustomAndroidScript):
    """
    启动初始化操作
    :param driver:
    :return:
    """
    createFold('./data/temp')
    # 传送图片资源文件到手机
    imageSourcePath = r'./data/imageSource'
    imageFiles = os.listdir(imageSourcePath)
    for i in imageFiles:
        driver.push_file(os.path.join(imageSourcePath, i), driverBasePath + i)


# 7. 执行脚本，Pycharm 中，直接右键执行
if __name__ == '__main__':
    # 注意：此处监听的端口号，必须和手机端的脚本端口号一致；
    # 监听 3333 号端口
    CustomAndroidScript.execute(16678)
