# 1. 导入 AndroidBotMain 类
import time

from a01startAPPandEnterToSearchBar import *
from a02PerShop import *
from toolkit.fileOperation import createFold, listToTxt
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


def main(driver: CustomAndroidScript):
    """
    主函数
    :param driver:
    :return:
    """
    init(driver)
    cityList = loadXpath(r'./data/城市列表.txt')
    searchFor = loadXpath(r'./data/搜索内容.txt')[0]
    configDict = TxtToDict(r'./data/配置文件.txt')
    num = int(configDict["每个地区下采集多少个店铺"])
    cityListCopy = cityList.copy()
    for city in cityList:
        city = city.strip()
        print("开始切换城市..")
        switchCity(driver, city)  # 切换城市
        time.sleep(2)
        search(driver, searchFor)  # 搜索
        shopTraversal(driver, num=num, cityName=city)  # 进行店铺遍历
        # 回退到美团主页面
        for i in range(4):
            driver.back()
            time.sleep(1)
        driver.start_app("美团")
        time.sleep(5)
        # 每完成一个城市，将他删去并写入txt
        cityListCopy.pop(0)
        listToTxt(cityListCopy, r'./data/城市列表.txt')
    for i in range(10):
        print("------------")
    print("结束.....")


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
