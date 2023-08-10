import time

# 1. 导入 WebBotMain 类
from AiBot import WebBotMain


# 2. 自定义一个脚本类，继承 WebBotMain
class CustomWebScript(WebBotMain):
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
        # 6. API 演示
        # 注意：Python 版本支持的 Api 与 Nodejs 基本相同
        # 教程中仅演示部分 Api，更多 Api 请自行探索，所有 Api 均包含详细的参数要求和返回值，请自行查看。

        main(self)


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                       time_tuple[5])
    # return "{}年{}月{}日{}点{}分".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4])


def main(driver: CustomWebScript):
    f = open('urls.txt')
    urls = f.readlines()
    f.close()
    count = 1
    while True:
        for i in range(2400, len(urls)):
            url = urls[len(urls) - i - 1]
            driver.goto(url.strip())
            time.sleep(1)
            if "验证码拦截" in driver.get_current_title():
                time.sleep(5)
                # # 元素矩形位置
                # sdPos = driver.get_element_rect(xpath="""//*[@id="nc_1__bg"]""")
                # center = ((sdPos[0][0] + sdPos[1][0]) / 2, (sdPos[0][1] + sdPos[1][1]) / 2)
                # driver.click_mouse(center, typ=3)
                # driver.move_mouse((center[0] + 500, center[1]))
                # driver.click_mouse((center[0] + 500, center[1]), typ=4)
            temp = getCurrentTime()
            f = open('./log.txt', 'a')
            f.write(temp + '\t' + str(count) + "-" + driver.get_current_title() + url)
            f.close()
            print(temp + '\t' + str(count) + "-" + driver.get_current_title() + url.strip())
            count += 1


# 7. 执行脚本，Pycharm 中，直接右键执行
if __name__ == '__main__':
    # 启动脚本，监听 9999 号端口
    # 默认使用 Chrome 浏览器

    # local=True 时，是本地运行脚本，会自动启动 WebDriver.exe 驱动；
    # 在远端部署脚本时，请设置 local=False，手动启动 WebDriver.exe，启动 WebDriver.exe 时需指定远端 IP 或端口号；

    # 如本地部署脚本，需要传递 WebDriver 启动参数时，参考下面方式，如不需传递启动参数，则忽略：
    driver_params = {
        "browserName": "chrome",
        "debugPort": 0,
        "userDataDir": "./UserData",
        "browserPath": None,
        "argument": None,
    }

    CustomWebScript.execute(9999, local=True, driver_params=driver_params)
