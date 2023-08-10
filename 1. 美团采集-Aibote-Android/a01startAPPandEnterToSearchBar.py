import time
from AiBot import AndroidBotMain
from a02PerShop import shopOperation, itemTraversal
from toolkit.xlsxOperation import exchange, XLSX
from configTXT import TxtToDict

head = ["地区", "店铺链接", "店铺名", "地址", "电话", "证件号码", "企业名称", "店铺PDF", "商品链接", "商品名", "原价",
        "优惠价", "商品PDF"]
xlsxPath = exchange('./data')
xlsx = XLSX('./data/{}'.format(xlsxPath), head)
configDict = TxtToDict(r'./data/配置文件.txt')
numItems = int(configDict["每个店铺下采集多少个商品（热销商品下顺序进行）"])


def switchCity(driver: AndroidBotMain, cityName):
    cityName = cityName.strip()
    cityName = cityName.replace("市", "")
    cityName = cityName.replace("地区", "")
    # 进入选择页面
    switchCityBtnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=city_name"""
    driver.click_element(switchCityBtnXpath)
    time.sleep(1)
    # 输入城市名称
    searchBarXpath = """com.sankuai.meituan/com.sankuai.meituan:id=search_edit"""
    driver.click_element(xpath=searchBarXpath)
    driver.send_keys(cityName + '\n')
    time.sleep(1)
    # 点击第一个选项
    optionXpath = """com.sankuai.meituan/com.sankuai.meituan:id=tv_city_search_text"""
    driver.click_element(optionXpath)


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


def search(driver: AndroidBotMain, searchFor):
    searchFor = searchFor.strip()
    searchXpath = """com.sankuai.meituan/com.sankuai.meituan:id=search_edit_flipper"""
    driver.click_element(searchXpath)
    searchXpath = """com.sankuai.meituan/com.sankuai.meituan:id=search_hint"""
    driver.click_element(searchXpath)
    searchBarXpath = """com.sankuai.meituan/com.sankuai.meituan:id=search_edit"""
    driver.set_element_text(searchBarXpath, text=searchFor)
    print("开始搜索{}".format(searchFor))
    searchBtnXpath = """com.sankuai.meituan/com.sankuai.meituan:id=inner_search_button"""
    driver.click_element(searchBtnXpath, wait_time=5)


def printDict(perDict: dict):
    try:
        for i in perDict.keys():
            print("{}:{}".format(i, perDict[i]))
    except:
        a = 1


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                             time_tuple[5])
    # return "{}年{}月{}日{}点{}分".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4])


def enterNextShop(driver: AndroidBotMain, tryTime=10):
    """
    进入下一个店铺,成功返回True，失败返回False
    :param driver:
    :param tryTime:
    :return:
    """
    shopEnterXpath = """com.sankuai.meituan/com.sankuai.meituan:id=search_result_dynamic_item_litho_view[1]/android.view.ViewGroup"""
    for i in range(tryTime):
        if driver.find_images("店铺选择截图.png", wait_time=1, similarity=0.95) != []:  # 如果能找到上一次的图片
            slide(driver, 300)
            time.sleep(1)
        else:
            break
        if i == tryTime - 1:
            return False
    # 进入下一个店铺
    driver.save_element_screenshot(image_name="店铺选择截图.png", xpath=shopEnterXpath)
    driver.click_element(shopEnterXpath, wait_time=0.5)
    return True


def shopTraversal(driver: AndroidBotMain, num, cityName):
    """
    对搜索结果下的商店进行遍历
    :param cityName:
    :param driver:
    :param num:遍历数量
    :return:
    """
    time.sleep(3)
    slide(driver, 500)
    # head = ["地区", "店铺链接", "店铺名", "地址", "电话", "证件号码", "企业名称", "商品链接", "商品名", "原价", "优惠价"]
    for count in range(num):
        flag = enterNextShop(driver, tryTime=5)
        if not flag:
            break  # 如果进入下一个店铺失败，则退出循环
        # 店铺操作
        print("-----------店铺操作------------")
        print(getCurrentTime())
        time.sleep(3)
        try:
            shopInfo = shopOperation(driver, cityName=cityName)
        except:
            shopInfo = {}
        printDict(shopInfo)
        try:
            if shopInfo == {}:
                itemInfo = {}
            else:
                itemInfo = itemTraversal(driver, numItems, shopName=tryReadDict(shopInfo, "店铺名"))
        except:
            itemInfo = [{}]
        for i in itemInfo:
            print('------')
            printDict(i)
        while driver.get_activity() != ".search.result.SearchResultActivity":
            driver.back()
            time.sleep(1)
        slide(driver, 300)
        time.sleep(2)
        if itemInfo != [{}] and itemInfo != {}:
            xlsx.writeLine(infoMerge(shopInfo, itemInfo, cityName))  # 写入表格
        # # itemInfo和shopInfo全为空，则没有相关的搜索结果
        # if itemInfo == {} and shopInfo == {}:
        #     break


def tryReadDict(temp, key):
    try:
        return temp[key]
    except:
        return " "


def infoMerge(shopInfo: dict, itemInfo, cityName):
    hyperLink = """=HYPERLINK("{}", "PDF")"""
    result = ["", cityName]
    result.append(tryReadDict(shopInfo, "店铺链接"))
    result.append(tryReadDict(shopInfo, "店铺名"))
    result.append(tryReadDict(shopInfo, "地址"))
    result.append(tryReadDict(shopInfo, "电话"))
    result.append(tryReadDict(shopInfo, "证件号码:"))
    result.append(tryReadDict(shopInfo, "企业名称:"))
    pdfPath = tryReadDict(shopInfo, "店铺PDF")
    # result.append("""=HYPERLINK("{}", "店铺PDF")""".format(pdfPath))
    result.append(pdfPath)
    for item in itemInfo:
        result.append(tryReadDict(item, "商品链接"))
        result.append(tryReadDict(item, "商品名"))
        result.append(tryReadDict(item, "原价"))
        result.append(tryReadDict(item, "优惠价"))
        pdfPath = tryReadDict(item, "商品PDF")
        # result.append("""=HYPERLINK("{}", "商品PDF")""".format(pdfPath))
        result.append(pdfPath)
    return result
