import re

from bs4 import BeautifulSoup
from html.parser import HTMLParser
from driverOperation import *

html1 = """<tr><td>1110106002023021136490869</td><td>北京华博医院 </td><td>海氏海诺创可贴保护膜创口贴液体敷料10ml防水伤口愈合儿童透明A </td><td 
class="fn-color-999">2023-02-11 </td><td class="fn-color-org">待核查</td><td><div class="btnbox"><a 
href="/cuser/portal/case/detail?id=1110106002023021136490869" target="_blank">详情</a><a href="javascript:void(0)" 
id="1110106002023021136490869" onclick="open_clbcDia(&quot;1110106002023021136490869&quot;)">材料补充</a></div></td></tr> 
"""
html2 = """<tr><td>1440113002023021199119267</td><td>广州瑞果生物科技有限公司 </td><td>瑞果山茶油护肤4件套口水疹婴儿润肤霜抚触油3合一洗发沐浴护肤油 </td><td 
class="fn-color-999">2023-02-11 </td><td class="fn-color-green2">处理完成</td><td><div class="btnbox"><a 
href="/cuser/portal/case/detail?id=1440113002023021199119267" target="_blank">详情</a></div></td></tr> """
html3 = """<tr><td>1440106002023021117639604</td><td>广州市鑫翔贸易有限公司 </td><td>润本婴儿唇周膏宝宝新生儿口水护肤护唇特护膏保湿滋润疹面霜 </td><td 
class="fn-color-999">2023-02-11 </td><td class="fn-color-org">待核查</td><td><div class="btnbox"><a 
href="/cuser/portal/case/detail?id=1440106002023021117639604" target="_blank">详情</a><a href="javascript:void(0)" 
id="1440106002023021117639604" onclick="open_clbcDia(&quot;1440106002023021117639604&quot;)">材料补充</a></div></td></tr> 
"""


def getData(html):
    """
    获取目标html文本中的信息
    :return:
    """
    data = re.findall(""">(.*?)</td>""", html)
    number = data[0].split("<td>")[-1]
    operator = data[1]
    item = data[2]
    date = data[3]
    status = data[4]
    return number, operator, item, date, status


def enterInfo(driver, number, status):
    """
    PDF详情页面爬取
    :param driver:
    :param number:
    :param status:
    :return:
    """
    baseURL = "https://www.12315.cn/cuser/portal/case/detail?id="
    url = baseURL + number
    # addNewTab(driver, url)
    # switchWindow(driver, 2)
    driver.get(url)
    # orderNumber = ""  # 订单号
    # reason = ""  # 不立案原因
    # reportContent = ""  # 举报内容
    # processingUnit = ""  # 处理单位
    # processingUnitDetail = ""  # 处理单位详细
    # endDate = ""  # 结束时间

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'lxml')
    trs = soup.find_all('tr')
    dataDist = {}
    for i in trs:
        tds = i.find_all("td")
        dataDist[tds[0].text] = tds[1].text
    # if status == "不予立案":
    #     reason = xpath(driver, """/html/body/div[3]/div/div/div/div[3]/table/tbody/tr[3]/td[2]""").text
    # elif status == "处理完成":
    #     reason = xpath(driver, """/html/body/div[3]/div/div/div/div[2]/div[3]/table/tbody/tr[2]/td[2]""").text
    screenShotAll(driver, number)
    time.sleep(5)
    # driver.close()
    # switchWindow(driver, 1)
    return dataDist


# status: 待核查 已立案 不予立案 处理完成
def perMessage(driver, html):
    number, operator, item, date, status = getData(html)

    data = {"number": number, "operator": operator, "item": item, "date": date, "status": status}

    reason = ""
    if status == "待核查" or status == "已立案":
        return data
    elif status == "不予立案" or status == "处理完成":
        pdfDist = enterInfo(driver, number, status)
        for i in pdfDist:
            data[i] = pdfDist[i]
        return data
    else:
        print("-----其他原因")
