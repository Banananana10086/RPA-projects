import os

from selenium.webdriver.common.by import By
import time
from driverOperation import xpath
import re
from getCittNum import getCityNum
import difflib
import configparser
from gaudAPI import GaodeGeo

gd = GaodeGeo()
config = configparser.ConfigParser()
configPath = r"./config.ini"
config.read(configPath)

uploadWaitTime = int(config['asd']['uploadWaitTime'])
# specialCityList = config['asd']['specialCityList'].split(".")
specialCityList = []
key = config['asd']['key']


def selectItem(driver, itemClass):  # 选择商品类别
    driver.find_element(by=By.XPATH, value='//*[@id="xffwlx"]').clear()
    driver.find_element(by=By.XPATH, value='//*[@id="xffwlx"]').send_keys(itemClass)
    time.sleep(1)
    xpath(driver, r"""//*[@id="xffwlxUl"]/li[1]""").click()  # 搜索结果的第一个


def selectIssueClass(driver, issue):  # 举报问题类别
    xpath(driver, """//*[@id="tswtlx"]""").clear()
    xpath(driver, """//*[@id="tswtlx"]""").send_keys(issue)
    time.sleep(1)
    xpath(driver, r"""//*[@id="wtwlxUl"]/li""").click()  # 搜索结果的第一个
    return 0


def selectProvince(driver, num):  # 选择一级行政区
    temp = [8, 9, 9, 5]
    province = driver.find_element(by=By.XPATH, value='//*[@id="cldwdiv"]/div[1]/div/div[2]/div[1]')
    provinceCode = province.get_attribute("innerHTML")
    codeList = re.findall(r'data-code="(.*?)" class=', provinceCode)
    i = 0
    for i in range(len(codeList)):
        if codeList[i][:2] == num[:2]:
            break
    i = i + 1
    a = 1
    b = 1
    for j in temp:
        if j >= i:
            b = i
            break
        else:
            i = i - j
            a += 1
    # print(a, b)
    xpath(driver, """//*[@id="cldwdiv"]/span""").click()
    # print(xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[1]/dl[{}]/dd/a[{}]""".format(a, b)).text)
    xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[1]/dl[{}]/dd/a[{}]""".format(a, b)).click()


def selectCity(driver, num):  # 选择第二行政区
    city = xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[2]/dl/dd""")
    city = city.get_attribute("innerHTML")
    cityCode = re.findall(r"""data-code="(.*?)" class=""", city)
    if len(cityCode) == 1:
        xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[2]/dl/dd/a[1]""").click()
        return
    i = 0
    for i in range(len(cityCode)):
        if cityCode[i][2:4] == num[2:4]:
            break
    i += 1
    # print(xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[2]/dl/dd/a[{}]""".format(i)).text)
    xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[2]/dl/dd/a[{}]""".format(i)).click()


def selectProcessingUnitByCode(driver, code):
    district = xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd""")
    district = district.get_attribute("innerHTML")
    districtCode = re.findall(r"""data-code="(.*?)" class=""", district)
    i = 0
    for i in range(len(districtCode)):
        if districtCode[i][4:6] == code[4:6]:
            break
    i += 1
    xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd/a[{}]""".format(i)).click()


def selectProcessingUnit(driver, name):
    unit = xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd""")
    unit = unit.get_attribute("innerHTML")
    unit = re.findall("""<a title="(.*?)" data-code=""", unit)
    temp = []
    for i in range(len(unit)):
        temp.append(difflib.SequenceMatcher(None, name, unit[i]).quick_ratio())
    maxIndex = temp.index(max(temp))
    maxIndex += 1
    # print(xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd/a[{}]""".format(i)).text)
    xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd/a[{}]""".format(maxIndex)).click()


def specialCityContains(cityName):
    """
    是否包含特殊的地址名字\n
    :param cityName:
    :return:
    """
    for temp in specialCityList:
        if temp in cityName:  # 如果有则返回包含的特殊的城市的名字
            return temp
    return ""  # 否则返回空字符串


def selectUnit(driver, address, unitName):
    if "重庆" in address:  # 重庆市是唯一有两个区的直辖市
        cityNumList = ['500100', '500200']
        for i in cityNumList:
            try:
                selectProvince(driver, i)
                selectCity(driver, i)
                name = unitName.replace("重庆", "")
                name = name.replace("市", "")
                name = name.replace("区", "")
                name = name[:2]
                unit = xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd""")
                unit = unit.get_attribute("innerHTML")
                unit = re.findall("""<a title="(.*?)" data-code=""", unit)
                index = 0
                for i in range(len(unit)):
                    if name in unit[i]:
                        index = i + 1
                        break
                # print(xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd/a[{}]""".format(i)).text)
                if index != 0:
                    xpath(driver, """//*[@id="cldwdiv"]/div[1]/div/div[2]/div[3]/dl/dd/a[{}]""".format(index)).click()
                    break
            except:
                a = 1
        return
    else:
        cityNumList = getCityNum(address)
    for i in cityNumList:
        try:
            selectProvince(driver, i)
            selectCity(driver, i)
            sCity = specialCityContains(address)
            if sCity != "":
                selectProcessingUnit(driver, address.replace(sCity, ""))
            else:
                selectProcessingUnit(driver, unitName)
        except:
            a = 1


def selectUnit2(driver, address, unitName):
    data = gd.getGeoCode(address)
    province = data['geocodes'][0]['province']
    city = data['geocodes'][0]['city']
    district = data['geocodes'][0]['district']
    adcode = data['geocodes'][0]['adcode']
    selectProvince(driver, adcode)
    selectCity(driver, adcode)
    if "高新" in unitName or "开发" in unitName or "技术" in unitName or "开发" in unitName or "经济" in unitName or "新区" in unitName + district == None:
        unitName = unitName.replace(province, "")
        unitName = unitName.replace(city, "")
        unitName = unitName.replace(province.replace("省", ""), "")
        unitName = unitName.replace(city.replace("市", ""), "")
        unitName = unitName.replace("市场", "")
        unitName = unitName.replace("监督", "")
        unitName = unitName.replace("管理", "")
        unitName = unitName.replace("监管", "")
        unitName = unitName.replace("经济", "")
        unitName = unitName.replace("局", "")
        selectProcessingUnit(driver, unitName)
    else:
        selectProcessingUnitByCode(driver, adcode)
    # try:  # 选推荐处理单位
    #     xpath(driver, """//*[@id="cldwTr"]/td/div[2]""").click()
    #     xpath(driver, """//*[@id="cldwtipdiv"]/div/div[2]/a[1]""").click()
    # except:
    #     a = 1


def selectSaleMode(driver, mode, info):
    xpath(driver, """//*[@id="salemode"]""").click()
    xpath(driver, """//*[@id="xsfsliDiv"]/ul/li[1]/a""").click()
    xpath(driver, """//*[@id="dsptname"]""").click()
    if "商家" in info:  # 纠错
        info = "入驻商户"
    # 获得所有商户列表
    shopList = []
    shopElems = driver.find_elements(by=By.CLASS_NAME, value="""dspt_data_a""")
    for elem in shopElems:
        shopList.append(elem.text)
    # 确实是第几个商户
    num = 1
    for shop in shopList:
        if mode in shop:
            break
        num += 1
    xpath(driver, """//*[@id="dspt_data"]/div/a[{}]""".format(num)).click()
    # 选择下方的类型
    checkList = []
    checkElems = driver.find_elements(by=By.CLASS_NAME, value="""check-item""")
    for check in checkElems:
        checkList.append(check.text)
    num = 1
    for check in checkList:
        if info in check:
            break
        num += 1
    xpath(driver, """//*[@id="dspt_data"]/div/div/a[{}]""".format(num)).click()
    xpath(driver, """// *[ @ id = "dspt_submit_btn"]""").click()  # 确定


def runPerData(driver, fileName):
    ########### 新
    # 文件读取操作
    f = open(fileName)
    string = f.readlines()
    new = []
    for i in string:
        if i != "\n":
            new.append(i)
    companyName = new[0].strip()
    itemName = new[3].strip()
    itemClass = new[4].strip()
    issueClass = new[5].strip()
    issueClass = issueClass.split('-')[-1]
    # orderNum = new[-1]
    words = companyName + new[1].strip()
    try:
        saleMode = new[6].strip()
    except:
        saleMode = "天猫"
    try:
        saleModeInfo = new[7].strip()
    except:
        saleModeInfo = "投诉商家"
    f.close()
    # else:
    #     ########### 旧
    #     # 文件读取操作
    #     f = open(fileName)
    #     string = f.readlines()
    #     new = []
    #     for i in string:
    #         if i != "\n":
    #             new.append(i)
    #     companyName = new[0].strip()
    #     itemName = new[-2].strip()
    #     itemClass = "诊断药品"
    #     issueClass = new[-1].strip()
    #     issueClass = issueClass.split("-")[-1]
    #     words = companyName + new[1].strip()
    #     f.close()

    # 进入举报界面
    driver.get("https://www.12315.cn/cuser/portal/jbcase/corperation")
    xpath(driver, """//*[@id="searchBox"]""").clear()
    xpath(driver, """//*[@id="searchBox"]""").send_keys(companyName)
    xpath(driver, """//*[@id="main_content"]/div[1]/div[4]""").click()  # 点击搜索
    try:
        xpath(driver, """//*[@id="searchResult"]/li/a""").click()  # 进入搜索结果
    except:
        xpath(driver, """//*[@id="searchResult"]/li[1]/a""").click()
    # time.sleep(3)
    address = xpath(driver, """//*[@id="confirm"]/table/tbody/tr[3]/td[2]""").text
    unitName = xpath(driver, """//*[@id="confirm"]/table/tbody/tr[4]/td[2]""").text
    # 数据最后一行是否有地址 例如：某某省/某某市/某某区市场监督管理局
    try:
        temp = new[8].strip()
        temp = temp.split("/")
        address = temp[0] + temp[1] + temp[-1]
        unitName = temp[-1]
    except:
        a = 1

    xpath(driver, """//*[@id="corperationSave"]""").click()  # 确认
    if xpath(driver, """//*[@id="provideraddr"]""").get_attribute('value') == "":
        xpath(driver, """//*[@id="provideraddr"]""").send_keys("河南省三门峡市湖滨区涧河街道")
    xpath(driver, """//*[@id="customerSubmit"]""").click()  # 提交
    #######################################################
    # 输入信息
    # 输入商品名
    xpath(driver, """//*[@id="spmc"]""").clear()
    if len(itemName) >= 50:
        xpath(driver, """//*[@id="spmc"]""").send_keys(itemName[0:49])
    else:
        xpath(driver, """//*[@id="spmc"]""").send_keys(itemName)
    selectItem(driver, itemClass=itemClass)
    selectIssueClass(driver, issue=issueClass)
    time.sleep(1)
    xpath(driver, """//*[@id="tsnr"]""").click()
    xpath(driver, """//*[@id="tsnr"]""").clear()
    xpath(driver, """//*[@id="tsnr"]""").send_keys(words)
    time.sleep(1)
    ############################################
    # print("开始选择处理单位：", address, unitName)
    selectUnit2(driver, address, unitName)
    time.sleep(1)
    # 选择销售模式
    selectSaleMode(driver, saleMode, saleModeInfo)
    # 填写订单号
    # xpath(driver, """//*[@id="ddh"]""").clear()
    # xpath(driver, """//*[@id="ddh"]""").send_keys(orderNum)

    # 上传文件
    pdfName = ""
    fatherPath = os.path.dirname(fileName)
    files = os.listdir(fatherPath)
    for i in files:
        if '.pdf' in i:
            pdfName = i
            os.system(r"""copy "{}" D:""".format(os.path.join(fatherPath, pdfName)))
            driver.find_element(by=By.CLASS_NAME, value="webuploader-element-invisible").send_keys(
                r"D:\{}".format(pdfName))
            time.sleep(2)

    # 提交
    xpath(driver, """/html/body/div[3]/div/div[2]/div/div[2]/div[2]/input""").click()
    time.sleep(uploadWaitTime)
    try:
        os.remove(r"D:\{}".format(pdfName))
    except:
        a = 1

    temp = xpath(driver, """/html/body/div[3]/div/div/div[1]/dl/dd""").text  # 判断是否提交成功
