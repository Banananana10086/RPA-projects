from selenium.webdriver.common.by import By
import time
from driverOperation import xpath, login, logout
from fileOperation import removeSpecialCharLess, findFilesBasisSuffix
from selenium.webdriver.support.select import Select
import os
from gaudAPI import GaodeGeo

gd = GaodeGeo()


def pressComplaint(driver, startTime, endTime, isPermanent=False):
    """
    在登录成功之后，点击投诉请求按钮，并校验身份证有效日期\n
    :param driver:
    :param startTime: 开始日期 (yyyy/mm/dd)
    :param endTime: 结束日期 (yyyy/mm/dd)
    :param isPermanent: (bool) 是否长期有效
    :return:
    """
    btnComplaint = xpath(driver, """//*[@id="tousuBtn"]""")
    btnComplaint.click()
    startTimeInput = xpath(driver, """//*[@id="csrq1"]""")
    if isPermanent:  # 如果是长期有效的
        xpath(driver, """//*[@id="jiaoyan-dialog"]/div[1]/div/div[2]/div/div[1]/i""").click()
        startTimeInput.clear()
        startTimeInput.send_keys(startTime)
    else:  # 如果不是长期有效的
        xpath(driver, """//*[@id="jiaoyan-dialog"]/div[1]/div/div[2]/div/div[2]/i""").click()
        startTimeInput.clear()
        startTimeInput.send_keys(startTime)
        endTimeInput = xpath(driver, """//*[@id="csrq2"]""")
        endTimeInput.clear()
        endTimeInput.send_keys(endTime)
    xpath(driver, """//*[@id="jyqdBtn"]""").click()  # 点击确定按钮
    time.sleep(2)
    try:
        xpath(driver, """//*[@id="tousuxuzhi-dialog"]/div[2]/div/div/div[1]/div/i""").click()  # 勾选同意
        xpath(driver, """//*[@id="isAbledBtn"]""").click()  # 点击同意
    except:
        xpath(driver, """//*[@id="tousuxuzhi-dialog"]/div[2]/div/div/div[1]/div/i""").click()  # 勾选同意
        xpath(driver, """//*[@id="isAbledBtn"]""").click()  # 点击同意
    time.sleep(3)


def occurrencePlace(driver, address, type):
    """
    选择事发地\n
    :param driver:
    :param address:
    :return:
    """
    if type == 1:  # 要求解决某事
        xpathParList = ["""//*[@id="province"]""", """//*[@id="city"]""", """//*[@id="district"]""",
                        """//*[@id="wtsdbc1"]"""]
    else:  # 不同意处理某事
        xpathParList = ["""//*[@id="province1"]""", """//*[@id="city1"]""", """//*[@id="district1"]""",
                        """//*[@id="wtsdbc2"]"""]

    # 普通方法
    # address = address.split('/')
    # print('--- 地址：', address)

    # # 第二方法
    # # print("--- 开始选择事发地")
    # df = cpca.transform([address])
    # dfList = list(df.loc[0])
    # address = []
    # for i in dfList:
    #     if i == None:
    #         dfList.append(" ")
    #     else:
    #         address.append(i)
    # address = address[:-1]
    #
    # province = address[0]
    # city = address[1]
    # district = address[2]
    # print(province, city, district)

    # 第三方法 高德地图API
    data = gd.getGeoCode(address)
    print(data)
    province = data['geocodes'][0]['province']
    city = data['geocodes'][0]['city']
    district = data['geocodes'][0]['district']
    adcode = data['geocodes'][0]['adcode']
    print(province, city, district, adcode)

    # # 选择第一第二行政区
    # provinceSelect = Select(xpath(driver, xpathParList[0]))
    # firstOption = province
    # for option in provinceSelect.options:
    #     if province[:2] in option.text:
    #         firstOption = option.text
    # provinceSelect.select_by_visible_text(firstOption)
    # # 第二
    # citySelect = Select(xpath(driver, xpathParList[1]))
    # secondOption = city
    # for option in citySelect.options:
    #     if city[:2] in option.text:
    #         secondOption = option.text
    # citySelect.select_by_visible_text(secondOption)
    # # 选择第三行政区
    # districtSelect = Select(xpath(driver, xpathParList[2]))
    # thirdOption = ""
    # for option in districtSelect.options:
    #     if district[:2] in option.text:
    #         thirdOption = option.text
    # districtSelect.select_by_visible_text(thirdOption)

    # 根据行政区号选择地区
    # 第一
    try:
        provinceSelect = Select(xpath(driver, xpathParList[0]))
        provinceSelect.select_by_value(adcode[0:2] + '0000')
    except:
        a = 1
    # 第二
    try:
        citySelect = Select(xpath(driver, xpathParList[1]))
        citySelect.select_by_value(adcode[0:4] + '00')
    except:
        a = 1
    # 第三
    try:
        districtSelect = Select(xpath(driver, xpathParList[2]))
        districtSelect.select_by_value(adcode[0:6])
    except:
        a = 1
    # 输入详细地址
    forthAddress = address[-1]
    xpath(driver, xpathParList[3]).clear()
    xpath(driver, xpathParList[3]).send_keys(address)


def problemCategory(driver, issue, type):
    """
    选择问题类别
    已经将“互联网信息管理”纠正为“互联网信息监管”\n
    :param driver:
    :param issue:
    :return:
    """
    if type == 1:  # 要解决某事
        xpathParr = """//*[@id="cascade_{}"]"""
    else:  # 不同意处理某事
        xpathParr = """//*[@id="cascade2_{}"]"""
    # 1 //*[@id="cascade2_0"] 第一选择框
    # 2 //*[@id="cascade2_1"] 第二
    # 3 //*[@id="cascade2_2"] 第三（可能没有）第四（可能没有）
    issue = issue.split("-")
    for num in range(len(issue)):
        webElemSelector = Select(xpath(driver, xpathParr.format(num)))
        if issue[num] == "互联网信息管理":  # 文本中出错的地方
            webElemSelector.select_by_visible_text("互联网信息监管")
        else:
            webElemSelector.select_by_visible_text(issue[num])


def isLayUiExist(driver):
    try:
        driver.find_element(by=By.CLASS_NAME, value="""layui-layer-content""")
        return True
    except:
        return False


def documentUpload(driver, foldName, type):
    """
    上传文件夹下面的所有pdf文件\n
    :param driver:
    :param foldName:
    :return:
    """
    if type == 1:  # 要解决某事
        uploadXpathPar = """//*[@id="qjform"]/div[12]/div[2]/input"""
    else:
        uploadXpathPar = """//*[@id="ssform"]/div[12]/div[2]/input"""
    pdfPaths = findFilesBasisSuffix(foldName, "pdf")
    for i in range(len(pdfPaths)):
        pdfPaths[i] = foldName + '/' + pdfPaths[i]
    uploadElem = xpath(driver, uploadXpathPar)
    for pdfPath in pdfPaths:
        uploadElem.send_keys(os.path.abspath(pdfPath))
        while not isLayUiExist(driver):  # 提交之后等待提示框出现
            continue
        time.sleep(0.3)
        print("---", driver.find_element(by=By.CLASS_NAME, value="""layui-layer-content""").text, foldName + "/" +
              pdfPath.split('/')[-1])
        if "出错" in driver.find_element(by=By.CLASS_NAME, value="""layui-layer-content""").text:
            return False
        driver.find_element(by=By.CLASS_NAME, value="""layui-layer-btn0""").click()
    return True


def perAccount(driver, name, personMessage, txtPath):
    """
    对于每条数据，或者说是每个账户的操作\n
    :return:
    """
    f = open(txtPath)
    string = f.readlines()
    f.close()
    newString = []
    for stringTemp in string:
        if removeSpecialCharLess(stringTemp) != '':
            newString.append(removeSpecialCharLess(stringTemp))
    materials = {}
    materials["事实和理由"] = newString[0]
    materials["主要诉求"] = newString[1]
    materials["事发地"] = newString[2]
    materials["问题类别"] = newString[3]
    print("--- 事实和理由：", newString[0])
    print("--- 主要诉求：", newString[1])
    print("--- 事发地：", newString[2])
    print("--- 问题类别：", newString[3])
    # 登录
    login(driver, name, personMessage[0], personMessage[1])
    # 点击投诉请求按钮
    pressComplaint(driver, personMessage[2], personMessage[3])
    # 再次点击投诉请求按钮
    driver.get("https://wsxf.gjxfj.gov.cn/page/tsqq.html")
    # 进入选择信访目的
    mission = newString[-1]
    type = 0
    if "不服" in mission or "不同意" in mission:
        xpath(driver, """/html/body/div[2]/div[2]/div[2]/div[2]/a[2]/div/img""").click()
        type = 0  # 不同意某处理决定
    else:
        xpath(driver, """/html/body/div[2]/div[2]/div[2]/div[2]/a[1]/div/img""").click()
        type = 1  # 要求解决某事
    time.sleep(3)  # 等待网页加载
    # 投诉请求：选择事发地
    occurrencePlace(driver, materials["事发地"], type)
    # 投诉请求：选择问题类别
    problemCategory(driver, materials["问题类别"], type)
    # 投诉请求：主要诉求
    if type == 0:  # 不同意某处理决定
        xpath(driver, """//*[@id="ssbf1"]""").clear()
        xpath(driver, """//*[@id="ssbf1"]""").send_keys(materials["主要诉求"])
    else:
        xpath(driver, """//*[@id="qjnr"]""").clear()
        xpath(driver, """//*[@id="qjnr"]""").send_keys(materials["主要诉求"])
    # 投诉请求：事实和理由
    if type == 0:  # 不同意某处理决定
        xpath(driver, """//*[@id="ssly1"]""").clear()
        xpath(driver, """//*[@id="ssly1"]""").send_keys(materials["事实和理由"])
    else:
        xpath(driver, """//*[@id="ssly"]""").clear()
        xpath(driver, """//*[@id="ssly"]""").send_keys(materials["事实和理由"])
    # 上传文件
    foldPath = r"{}".format(('/').join(txtPath.split("/")[:-1]))
    flag = documentUpload(driver, foldPath, type)
    if flag == False:  # 如果上传失败
        return False
    # 提交预览
    if type == 1:  # 要解决某事
        xpath(driver, """//*[@id="qjform"]/div[13]/button""").click()
    else:
        xpath(driver, """//*[@id="ssform"]/div[13]/button""").click()
    time.sleep(3)
    # 确定提交 //*[@id="ssDialog"]/div/form/div[12]/button[1]
    if type == 1:  # 要解决某事
        xpath(driver, """//*[@id="qjDialog"]/div/form/div[12]/button[1]""").click()
    else:
        xpath(driver, """//*[@id="ssDialog"]/div/form/div[12]/button[1]""").click()
    # 提示框确定提交
    driver.find_element(by=By.CLASS_NAME, value="""layui-layer-btn0""").click()
    return True
