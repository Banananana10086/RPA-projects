from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import ddddocr

ocr = ddddocr.DdddOcr()


def driverInit():
    """
    浏览器初始化
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
    driver.find_element_by_xpath 便捷方法
    """
    return dr.find_element(by=By.XPATH, value=val)


def isLoginSeccess(driver):
    # 如果登录失败会弹出提示框
    try:
        alert = driver.switch_to.alert
        print("登录错误信息", alert.text)
        return False
    except:
        return True


# login(driver, "钟英杰", "653130199604263679", "w1998523")
def login(driver, name, idNum, password):
    """
    登录操作，会进行多此尝试\n
    :param driver:
    :param name:
    :param idNum:
    :param password:
    :return:
    """
    url = "https://wsxf.gjxfj.gov.cn/"
    driver.get(url)
    time.sleep(3)
    # 输入姓名、证件号码、密码
    nameInput = xpath(driver, """//*[@id="tab_username"]""")
    nameInput.clear()
    nameInput.send_keys(name)
    idNumInput = xpath(driver, """//*[@id="tab_IDcard"]""")
    idNumInput.clear()
    idNumInput.send_keys(idNum)
    passwordInput = xpath(driver, """//*[@id="tab_password"]""")
    passwordInput.clear()
    passwordInput.send_keys(password)
    # 输入验证码
    xpath(driver, """//*[@id="login_div_id"]""").screenshot("D:/验证码.png")
    with open('D:/验证码.png', 'rb') as f:
        img_bytes = f.read()
    valCode = ocr.classification(img_bytes)
    valInput = xpath(driver, """//*[@id="tab1_yzm"]""")
    valInput.clear()
    valInput.send_keys(valCode)
    # 登录按钮
    loginBtn = xpath(driver, """//*[@id="hasLogin"]/div[2]/div[1]/button""")
    loginBtn.click()
    time.sleep(3)
    # 判断是否登录成功
    flag = 0
    while not isLoginSeccess(driver):
        if flag == 4:
            break
        alert = driver.switch_to.alert
        alert.accept()
        # 重新输入验证码并点击登录按钮
        xpath(driver, """//*[@id="login_div_id"]""").click()
        time.sleep(2)
        xpath(driver, """//*[@id="login_div_id"]""").screenshot("D:/验证码.png")
        with open('D:/验证码.png', 'rb') as f:
            img_bytes = f.read()
        valCode = ocr.classification(img_bytes)
        valInput = xpath(driver, """//*[@id="tab1_yzm"]""")
        valInput.clear()
        valInput.send_keys(valCode)
        # 登录按钮
        loginBtn = xpath(driver, """//*[@id="hasLogin"]/div[2]/div[1]/button""")
        loginBtn.click()
        time.sleep(3)
        flag += 1
    print("--- 登录成功:", name, idNum)


def logout(driver):
    """
    退出登录信访平台\n
    :param driver:
    :return:
    """
    url = "https://wsxf.gjxfj.gov.cn/"
    driver.get(url)
    logoutBtn = driver.find_elements(by=By.CLASS_NAME, value="""btn-box""")
    logoutBtn[0].click()
    xpath(driver, """//*[@id="layui-layer1"]/div[3]/a[1]""").click()
    print("--- 退出登录")
