from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import ddddocr

ocr = ddddocr.DdddOcr()


def driverInit():
    """
    浏览器初始化\n
    """
    options = webdriver.ChromeOptions()  # 创建一个配置对象
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    # mobileEmulation = {'deviceName': 'iPhone 6'}
    # options.add_experimental_option('mobileEmulation', mobileEmulation)
    driver = webdriver.Chrome(options=options)  # 实例化带有配置的driver对象
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """
                       ![](../../../AppData/Local/Temp/O1CN01Z2ISWv1nZDuBAyo1n_!!0-item_pic.jpg_790x10000q50.jpg) Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """})
    driver.implicitly_wait(5)
    driver.set_window_size(1500, 800)
    return driver


def xpath(dr, val):
    """
    driver.find_element_by_xpath 便捷方法\n
    """
    return dr.find_element(by=By.XPATH, value=val)


def login(driver, num, key):
    driver.get("https://www.12315.cn/cuser/")
    xpath(driver, """//*[@id="loginForm"]/ul/li[1]/div/input""").clear()
    xpath(driver, """//*[@id="loginForm"]/ul/li[1]/div/input""").send_keys(num)
    xpath(driver, """//*[@id="loginForm"]/ul/li[2]/div/input""").clear()
    xpath(driver, """//*[@id="loginForm"]/ul/li[2]/div/input""").send_keys(key)

    valCode = ''
    xpath(driver, """//*[@id="loginForm"]/ul/li[3]/div""").click()
    time.sleep(0.5)
    xpath(driver, """//*[@id="cimg"]""").screenshot("D:/验证码.png")
    with open('D:/验证码.png', 'rb') as f:
        img_bytes = f.read()
    valCode = ocr.classification(img_bytes)
    xpath(driver, """//*[@id="code"]""").clear()
    xpath(driver, """//*[@id="code"]""").send_keys(valCode)
    xpath(driver, """//*[@id="loginSubmit"]""").click()
    time.sleep(2)


def isLoginSuccess(driver):
    """
    判断是否成功登录12315
    """
    driver.get("https://www.12315.cn/cuser/")
    try:
        temp = xpath(driver, """//*[@id="loginDiv"]/div/span""").text
    except:
        temp = ""
    if temp == "":
        return True
    else:
        return False

def logout(driver):
    """
    退出登录
    :param driver:
    :return:
    """
    driver.get("https://www.12315.cn/cuser/portal/logout")
