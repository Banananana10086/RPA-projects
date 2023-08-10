import time
from AiBot import AndroidBotMain
from toolkit.fileOperation import loadXpath, shopImageMerge, itemImageMerge
from toolkit.fileOperation import createFold, removeSpecialCharV2
import os
import re
from toolkit.config import config

shopNameXPathList = loadXpath(r'./data/xpathShopName.txt')
videoCloseXpathList = loadXpath(r'./data/xpathCloseVideo.txt')
driverBasePath = r"/storage/emulated/0/Android/data/com.aibot.client/files/"
sharBtnXpathList = loadXpath(r'./data/xpathShareBtn.txt')


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


def getScreenShotAndSendToPC(driver: AndroidBotMain, imageName, dataPath, region=None):
    driver.save_screenshot(image_name=imageName, region=region)
    driver.pull_file(remote_path=driverBasePath + imageName, local_path=os.path.join(dataPath, imageName))


def getShopName(driver: AndroidBotMain):
    """
    在店铺页面，获取店铺名称
    :param driver:
    :return:
    """
    shopNameXpath = """com.sankuai.meituan/com.sankuai.meituan:id=normal_cell_view/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[{}]/android.view.ViewGroup[{}]/android.widget.TextView"""
    temp = []
    for i in range(1, 7):
        for j in range(1, 7):
            temp.append(driver.get_element_text(shopNameXpath.format(i, j), wait_time=0.001, interval_time=0.001))
            temp.append(
                driver.get_element_text(shopNameXpath.format(i, j) + "[1]", wait_time=0.001, interval_time=0.001))
    asd = []
    for i in temp:
        if i != None:
            asd.append(i)
    shopName = ""
    for i in asd:
        try:
            temp = float(i)
            break
        except:
            shopName += i
    return shopName


def getCompanyInfo(driver: AndroidBotMain, ifGetInfo=0):
    """
    在店铺页面，获取店铺详情，包括证件号码和企业名称，并返回店铺页面
    :param ifGetInfo: 是否采集店铺资质 0表示不采集
    :param driver:
    :return:
    """
    # 如果不是在店铺详情页面，返回false
    if driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
        return False
    # 进入详情页面
    enterBtnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=normal_cell_view[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup"""
    driver.click_element(enterBtnXpath, wait_time=2)
    time.sleep(3)
    slide(driver, 300)
    time.sleep(0.5)
    # 医师列表
    drXpathList = [
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View/android.widget.TextView""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[5]/android.view.View/android.widget.TextView""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[6]/android.view.View/android.widget.TextView""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[7]/android.view.View/android.widget.TextView""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[1]/android.view.View""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[5]/android.view.View[1]/android.view.View""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[6]/android.view.View[1]/android.view.View""",
        """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[7]/android.view.View[1]/android.view.View"""]
    for drXpath in drXpathList:
        text = driver.get_element_text(drXpath, wait_time=0.5)
        if "医师" in str(text):
            driver.click_element(drXpath)
            time.sleep(5)
            driver.save_screenshot(image_name="医师资格审核.png")
            driver.back()
            break
        # print("获取医师详情出错")
    if ifGetInfo == 0:
        # 返回店铺页面
        while driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
            driver.back()
            time.sleep(1)
        return {}
    # 进入资质详情
    shopInfoXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.widget.TextView"""
    driver.click_element(shopInfoXpath, wait_time=2)
    time.sleep(2)
    # 如果出现验证码
    valCodeImageXpath = """com.sankuai.meituan/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.Image"""
    while driver.element_exists(valCodeImageXpath, wait_time=0.5):
        # 验证码操作
        # 断点
        input("出现验证码，点击回车继续....")
        # position = driver.get_element_rect(valCodeImageXpath)
        # driver.save_screenshot("验证码", (position[0][0], position[0][1], position[1][0], position[1][1]))
        # # 发送到电脑
        # driver.pull_file(driverBasePath + "验证码", r"./data/验证码")
        # valCode = ocr.predict('./data/验证码')
        # inputXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.EditText"""
        # driver.click_element(inputXpath)
        # time.sleep(1)
        # driver.send_keys(valCode)
        # btnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.widget.Button"""
        # position = driver.get_element_rect(btnXpath)
        # driver.click(((position[0][0] + position[1][0]) / 2, (position[0][1] + position[1][1]) / 2))
        # time.sleep(3)
        # shopInfoXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.widget.TextView"""
        # driver.click_element(shopInfoXpath, wait_time=0.5)

    # 获取信息
    time.sleep(2)
    result = {}
    infoXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.widget.TextView[{}]"""
    for i in range(1, 3):
        result[driver.get_element_text(infoXpath.format(2 * i - 1), wait_time=0.5)] = driver.get_element_text(
            infoXpath.format(2 * i), wait_time=0.5)
    # 返回店铺页面
    while driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
        driver.back()
        time.sleep(1)
    return result


def getShopLink(driver: AndroidBotMain):
    """
    在商品详情页面，获取店铺链接
    :param driver:
    :return:
    """
    if driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
        return False
    # 点击分享按钮
    for shareBtnXpath in sharBtnXpathList:
        driver.click_element(shareBtnXpath, wait_time=0.2)
    # 点击复制链接
    copyBtnXpath = """com.sankuai.meituan/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[4]/android.widget.ImageView"""
    driver.click_element(copyBtnXpath)
    time.sleep(2)
    temp = driver.get_clipboard_text()
    print('***', temp)
    result = {}
    result["店铺名"] = temp.split("，")[0]
    result["地址"] = temp.split("，")[1].split("：")[-1]
    result["电话"] = temp.split("，")[2].split("：")[-1].split("。")[0]
    result["店铺链接"] = temp.split(" ")[-1]
    return result


def tryReadDict(temp, key):
    try:
        return temp[key]
    except:
        return " "


def shopOperation(driver: AndroidBotMain, cityName):
    if driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
        return {}
    # 关闭可能存在的展示视频
    for videoCloseXpath in videoCloseXpathList:
        if driver.click_element(videoCloseXpath, wait_time=0.1, interval_time=0.1):
            break
    # 判断是否有精选商品一栏
    flag = locateToSelectedProducts(driver, tryTimes=5)
    if flag:
        for i in range(5):
            slide(driver, -500)
    else:
        return {}
    # 获取店铺链接
    time.sleep(2)
    try:
        shopInfo = getShopLink(driver)  # 店铺名\地址\电话\店铺链接
    except:
        print("--获取分享链接失败")
        return False
    shopName = shopInfo["店铺名"]
    # 获取店铺名
    # shopName = getShopName(driver)
    createFold('./data/temp/{}-{}'.format(cityName, shopName))
    dataPath = './data/temp/{}-{}'.format(cityName, shopName)
    # 截取店铺展示页
    time.sleep(1)
    driver.save_screenshot(image_name="店铺展示页.png")
    driver.pull_file(remote_path=driverBasePath + "店铺展示页.png", local_path=os.path.join(dataPath, "店铺展示页.png"))

    # 获取公司名和证件号码
    try:
        time.sleep(2)
        companyInfo = getCompanyInfo(driver, ifGetInfo=int(config['asd']['ifGetCompanyInfo']))  # 公司名\证件号码
        driver.pull_file(remote_path=driverBasePath + "医师资格审核.png",
                         local_path=os.path.join(dataPath, "医师资格审核.png"))
    except:
        print("--获取公司名、证件号码失败")
        return False
    shopInfo.update(companyInfo)
    # 合并图像并生成pdf
    pdfPath = shopImageMerge(dataPath, tryReadDict(shopInfo, "企业名称:"))
    shopInfo["店铺PDF"] = pdfPath
    # print(shopInfo)
    return shopInfo


def locateToSelectedProducts(driver: AndroidBotMain, tryTimes=5):
    """
    定位滑动到精选商品
    :param driver:
    :return:
    """
    global flag
    flag = -1
    txtXpath = """com.sankuai.meituan/com.sankuai.meituan:id=normal_cell_view[{}]/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView"""
    for count in range(tryTimes):
        for i in range(6):
            txt = driver.get_element_text(txtXpath.format(i), wait_time=0.2)
            if "精选商品" in str(txt):
                print(i, txt)
                flag = i
                break
        if flag != -1:
            return True
        slide(driver, 400)
        time.sleep(1)
    return False
    # # slide(driver, int(config['asd']['slide1']))
    # slide(driver, 300, waitTime=0.5)
    # txtXpath = """com.sankuai.meituan/com.sankuai.meituan:id=normal_cell_view[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView"""
    # count = 1
    # while driver.get_element_text(xpath=txtXpath, wait_time=0.1) != "精选商品":
    #     count += 1
    #     # slide(driver, int(config['asd']['slide2']), duration=float(config['asd']['slideDurationTime']),
    #     # waitTime=float(config['asd']['slideWaitTime']))
    #     slide(driver, 150, duration=float(config['asd']['slideDurationTime']),
    #           waitTime=float(config['asd']['slideWaitTime']))
    #     if count == 20:
    #         return False
    # return True


def clickShowMoreInfo(driver: AndroidBotMain, method=1):
    if method == 1:
        for i in range(5):
            position = driver.find_image("查看更多图文详情.png", wait_time=0.5, interval_time=0.2, similarity=0.8)
            if position != None:
                driver.click(position)
                break
            slide(driver, 500)
            time.sleep(1)
    elif method == 2:
        for i in range(3):
            slide(driver, 500)
            moreInfoBtnXpathList = [
                """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View/android.widget.TextView""",
                """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.TextView"""]
            for moreInfoBtnXpath in moreInfoBtnXpathList:
                text = driver.get_element_text(moreInfoBtnXpath, wait_time=0.5)
                if text == "查看更多图文详情":
                    driver.click_element(moreInfoBtnXpath)
                    break
    elif method == 3:
        selectBarXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[{}]/android.view.View/android.widget.TextView"""
        selectBarXpath1 = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[{}]/android.view.View"""
        # driver.click_element(selectBarXpath.format(0))
        # time.sleep(1)
        # driver.click_element(selectBarXpath.format(1))
        # time.sleep(1)
        driver.click_element(selectBarXpath.format(2))
        time.sleep(0.5)
        driver.click_element(selectBarXpath1.format(2))
        time.sleep(0.5)
        slide(driver, -150)
        time.sleep(2)
        shoreInfoXpathList = [
            """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.TextView""",
            """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View/android.widget.TextView""",
            """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View/android.widget.TextView""",
            """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.TextView"""]
        # shoreInfoXpath = driver.any_elements_exists(shoreInfoXpathList, wait_time=1, interval_time=0.1)
        # driver.click_element(shoreInfoXpath, wait_time=5)
        # driver.click_element(selectBarXpath.format(1))
        for shopNameXPath in shoreInfoXpathList:
            driver.click_element(shopNameXPath, wait_time=0.5)


def clickElemByPos(driver: AndroidBotMain, xpath, waitTime=2, offsetX=0, offsetY=0):
    """
    点击元素，先确定其坐标之后点击中心
    :param waiteTime:
    :param driver:
    :param xpath:
    :param offsetY:
    :param offsetX:
    :return:
    """
    pos = driver.get_element_rect(xpath, wait_time=waitTime)
    if pos == None:
        return False
    else:
        x = (pos[0].x + pos[1].x) / 2 + offsetX
        y = (pos[0].y + pos[1].y) / 2 + offsetY
        driver.click((x, y))
    return True


def itemOperation(driver: AndroidBotMain, shopName):
    if driver.get_activity() != """com.sankuai.titans.adapter.mtapp.KNBWebViewActivity""":
        print("不位于商品界面，无法进行操作")
        return False
    result = {}
    time.sleep(1)
    slide(driver, 800)
    slide(driver, 800)
    time.sleep(1)
    slide(driver, -800)
    slide(driver, -800)
    slide(driver, -800)
    time.sleep(2)
    # 分享链接信息提取
    shareBtnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=button_rr/android.widget.ImageView"""
    driver.click_element(shareBtnXpath, wait_time=3)
    time.sleep(int(config['asd']['waitTimeAfter']))
    copyBtnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=share_image[4]"""
    if config['asd']['typeOfClickShareBtn'] == "1":
        driver.click((968, 1736))
    else:
        try:
            driver.click_element(copyBtnXpath)  # 这一步可能会出错
        except:
            clickElemByPos(driver, copyBtnXpath)
    time.sleep(2)
    itemInfo = driver.get_clipboard_text()
    print('***', itemInfo)
    # 分享内容解析
    originalPrice = re.findall("""仅售(.*?)元""", itemInfo)[0]
    itemName = re.findall("""元，(.*?)http""", itemInfo)[0]
    itemLink = itemInfo.split(" ")[-1]
    result["原价"] = originalPrice
    result["商品名"] = itemName
    result["商品链接"] = itemLink
    # 创建文件夹
    foldName = removeSpecialCharV2(itemLink)
    createFold("./data/temp/{}".format(foldName))
    dataPath = "./data/temp/{}".format(foldName)
    getScreenShotAndSendToPC(driver, imageName="商品主页面.png", dataPath=dataPath)  # 保存主页面截图
    # # 获得优惠价
    # preferentialPriceXpathList = [
    #     """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.widget.TextView[1]""",
    #     """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.widget.TextView[1]"""]
    # preferentialPrice = ''
    # for tempXpath in preferentialPriceXpathList:
    #     preferentialPrice = driver.get_element_text(tempXpath, wait_time=0.2)
    #     # print(preferentialPrice)
    #     try:
    #         float(preferentialPrice)
    #         break
    #     except:
    #         continue
    result["优惠价"] = "0"
    # print(result)
    # 获取套餐详情
    slide(driver, 800)
    slide(driver, 800)
    slide(driver, 800)
    slide(driver, 800)
    time.sleep(0.5)
    selectBarXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[{}]/android.view.View/android.widget.TextView"""
    selectBarXpath1 = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[{}]/android.view.View"""
    driver.click_element(selectBarXpath.format(0))
    time.sleep(0.5)
    driver.click_element(selectBarXpath1.format(0))
    time.sleep(0.5)
    getScreenShotAndSendToPC(driver, imageName="套餐详情.png", dataPath=dataPath)
    # 获取图文介绍
    driver.click_element(selectBarXpath.format(1))
    driver.click_element(selectBarXpath1.format(1))
    clickShowMoreInfo(driver, method=3)  # 点击查看更多图文详情按钮
    # 判断需要截几张图并进行截图
    driver.click_element(selectBarXpath.format(1))  # 回到图文详情首页
    driver.click_element(selectBarXpath1.format(1))  # 回到图文详情首页
    time.sleep(0.5)
    count = 1
    tempXpath = """com.sankuai.meituan/com.sankuai.meituan:id=mil_container/android.webkit.WebView/android.webkit.WebView/android.view.View[2]/android.view.View/android.view.View/android.widget.TextView"""
    i = 1
    baseName = "商品图文介绍{}.png"
    while driver.get_element_text(tempXpath, wait_time=0.5) != "评价":
        getScreenShotAndSendToPC(driver, baseName.format(i), dataPath)
        i += 1
        slide(driver, 800)
        count += 1
        if i == 6:
            break
    getScreenShotAndSendToPC(driver, baseName.format(i), dataPath)
    # 生成PDF
    result["商品PDF"] = itemImageMerge(dataPath, shopName)
    return result


def itemTraversal(driver: AndroidBotMain, num: int, shopName):
    """
    商品遍历
    :param driver:
    :param num: 商品数目
    :return:
    """
    itemInfo = []
    if driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
        print("不位于店铺界面，无法进行操作")
    temp = locateToSelectedProducts(driver)
    if temp == True:
        print("成功定位到精选商品页面...")
    else:
        print("无法定位到精选商品页面...")
        return [{}]
    global flag
    itemEnterBtnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=normal_cell_view[{}]/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[{}]"""
    for count in range(num):
        driver.click_element(itemEnterBtnXpath.format(flag + 2, count))
        time.sleep(3)
        result = itemOperation(driver, shopName)
        itemInfo.append(result)
        while driver.get_activity() != """com.meituan.android.generalcategories.poi.GCPoiDetailAgentActivity""":
            driver.back()  # 返回商店页面
            time.sleep(1)
    return itemInfo
