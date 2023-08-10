import re

from driverOperation import *
from perMessage import perMessage

enterNextPageWaitTime = 0.3


def removeSpecialChar(temp):  # 删除特殊字符
    temp = temp.replace('/', '')
    temp = temp.replace("""\\""", '')
    temp = temp.replace(""":""", '')
    temp = temp.replace("""?""", '')
    temp = temp.replace('"', '')
    temp = temp.replace("""<""", '')
    temp = temp.replace(""">""", '')
    temp = temp.replace("""|""", '')
    temp = temp.replace("""*""", '')
    temp = temp.replace(""" """, '')
    temp = temp.replace("""\n""", '')
    temp = temp.replace("""\t""", '')
    return temp

def removeSpecialCharLess(temp):
    """
    删除换行和制表符\n
    :param temp:
    :return:
    """
    temp = temp.replace("""\n""", '')
    temp = temp.replace("""\t""", '')
    temp = temp.replace(""" """, '')
    return temp

def getMessageFromTOBDY(pageSource):
    pat = """<tr>(.*?)</tr>"""
    temp = re.findall(pat, pageSource)
    temp.remove(temp[0])
    return temp


def isRequireDate(htmlSource, requireDate):
    temp = re.findall(""">(.*?)</td>""", htmlSource)
    date = temp[3]
    date = removeSpecialChar(date)
    # 2023-02-15
    date = date.split("-")
    if int(date[0]) == int(requireDate[0]) and int(date[1]) == int(requireDate[1]) and int(date[2]) == int(
            requireDate[2]):
        return True
    elif int(date[0]) * 365 + int(date[1]) * 30 + int(date[2]) < \
            int(requireDate[0]) * 365 + int(requireDate[1]) * 30 + int(requireDate[2]):
        return "break"
    else:
        return False


def upperPartNextPageBtn(driver, maxPage):
    """
    点击下一页按钮
    :param driver:
    :param maxPage:
    :return:
    """
    # //*[@id="paging_his"]
    pageBarSource = xpath(driver, """//*[@id="paging"]""").get_attribute("outerHTML")
    currentPage = re.findall("""<li class="btn btnsmall current">(.*?)</li>""", pageBarSource)[0]
    currentPage = int(currentPage)
    if currentPage < maxPage:
        if maxPage >= 5:
            xpathPar = """//*[@id="paging"]/li[8]"""
        else:
            xpathPar = """//*[@id="paging"]/li[{}]""".format(3 + maxPage)
        xpath(driver, xpathPar).click()
        return True
    else:
        return False


def upperPart(driver, informList, requireDate):
    """
    采集半部分的所有信息
    :param driver:
    :param informList:
    :return:
    """
    pageBarSource = xpath(driver, """//*[@id="paging"]""").get_attribute("outerHTML")
    maxPage = re.findall('data-page=(.*?)href', pageBarSource)
    maxPage = removeSpecialChar(maxPage[-1])
    maxPage = int(maxPage)

    while True:
        pageSource = xpath(driver, """//*[@id="customerCaseGrid"]/tbody""").get_attribute("outerHTML")
        temp = getMessageFromTOBDY(pageSource)
        flag = True
        for i in temp:
            flag = isRequireDate(i, requireDate)
            if flag == True:
                informList.append(i)
            elif flag == "break":
                break
        if flag == 'break':
            break
        if not upperPartNextPageBtn(driver, maxPage):
            break
        time.sleep(enterNextPageWaitTime)


def downPartNextPageBtn(driver, maxPage):
    """
    点击下一页按钮

    :param driver:
    :param maxPage:
    :return:
    """
    # //*[@id="paging_his"]
    pageBarSource = xpath(driver, """//*[@id="paging_his"]""").get_attribute("outerHTML")
    currentPage = re.findall("""<li class="btn btnsmall current">(.*?)</li>""", pageBarSource)[0]
    currentPage = int(currentPage)
    if currentPage < maxPage:
        if maxPage >= 5:
            xpathPar = """//*[@id="paging_his"]/li[8]"""
        else:
            xpathPar = """//*[@id="paging_his"]/li[{}]""".format(3 + maxPage)
        xpath(driver, xpathPar).click()
        return True
    else:
        return False


def downPart(driver, informList, requireDate):
    """
    采集半部分的所有信息

    :param requireDate: (list) eg:[2000, 1, 1]
    :param driver:
    :param informList:
    :return:
    """
    pageBarSource = xpath(driver, """//*[@id="paging_his"]""").get_attribute("outerHTML")
    maxPage = re.findall('data-page=(.*?)href', pageBarSource)
    maxPage = removeSpecialChar(maxPage[-1])
    maxPage = int(maxPage)

    while True:
        pageSource = xpath(driver, """//*[@id="customerHisGrid"]/tbody""").get_attribute("outerHTML")
        temp = getMessageFromTOBDY(pageSource)
        flag = True
        for i in temp:
            flag = isRequireDate(i, requireDate)
            if flag == True:
                informList.append(i)
            elif flag == "break":
                break
        if flag == "break":
            break
        if not downPartNextPageBtn(driver, maxPage):
            break
        time.sleep(enterNextPageWaitTime)


def getMessage(driver, requireDate):
    """
    得到每一条信息的html源码

    :param driver:
    :param requireDate:
    :return:
    """
    driver.get("https://www.12315.cn/cuser/portal/")
    xpath(driver, """//*[@id="ulMenu"]/li[3]/a""").click()
    time.sleep(2)
    xpath(driver, """//*[@id="hisButton"]""").click()  # 查看历史按钮
    time.sleep(2)
    informList = []

    try:
        upperPart(driver, informList, requireDate)
    except:
        a = 1
    try:
        downPart(driver, informList, requireDate)
    except:
        a = 1
    return informList


def perAccount(driver, username, password, requireDate):
    while not isLoginSuccess(driver):
        login(driver, username, password)

    name = xpath(driver, """//*[@id="userName"]""").text
    data = getMessage(driver, requireDate)

    result = []
    for i in data:
        result.append(perMessage(driver, i))
    # 加入名字
    for i in result:
        i["name"] = name
        if i['status'] == "不予立案" or i['status'] == '处理完成':
            i["处理单位具体"] = i["处理单位"].split("/")[-1]
    return result
