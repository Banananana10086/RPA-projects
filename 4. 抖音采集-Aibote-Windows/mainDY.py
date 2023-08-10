# 1. 导入 WebBotMain 类
import time

from AiBot import WebBotMain

from config import config
from fileOperation import createFold, removeSpecialChar, png2png, png2PDF, delFileContainX, loadXpath
from xlsxOperation import *

# 初始化文件夹
createFold(r'data')
createFold(r"data/temp")
# 初始化xlsx
xlsxName = exchange('data')
xlsxPath = r'./data/{}'.format(xlsxName)
wb = load_workbook(xlsxPath)
sheet = wb[wb.sheetnames[0]]  # 选定第一个表
addHead(sheet, ['是否已经获取数据', '店铺名', 'PDF路径'])
wb.save(xlsxPath)

btnXpathList = loadXpath(r'./data/xpathBtn.txt')
infoXpathList = loadXpath(r'./data/xpathInfo.txt')
shopNameXpathList = loadXpath(r'./data/xpathShopName1.txt')


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
        print("-----------------------------------")
        print("程序运行完毕.......")


def saveImage(driver: WebBotMain, path, name, xpath=""):
    """
    保存图片\n
    :param driver:
    :param xpath:
    :param path:
    :param name:
    :return:
    """
    import base64
    from io import BytesIO
    from PIL import Image
    import os
    if xpath == "":
        b64str = driver.save_screenshot()
    else:
        b64str = driver.save_screenshot(xpath)
    image = base64.b64decode(b64str, altchars=None, validate=False)
    image = BytesIO(image)
    image = Image.open(image)
    image.save(os.path.join(path, name))


def urlToImage(url, path, name):
    import requests
    import os
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    path = os.path.join(path, name)
    maxCount = 5
    count = 0
    while r.status_code != 200:
        count += 1
        if count == maxCount:
            break
        time.sleep(1)
        print("请求过于频繁")
        r = requests.get(url, headers=headers)
    if r.status_code == 200:
        f = open(path, 'wb')
        f.write(r.content)
        f.close()


def saveShowImage(driver: WebBotMain, basePath):
    """
    保存所有展示的图片
    :param driver:
    :param basePath:
    :return:
    """
    import re
    eleHtml = driver.get_element_inner_html("""//*[@id="container"]/div[2]/div[1]/div/div""")
    imageUrls = re.findall("""&quot;(.*?)&quot;""", eleHtml)
    count = 1
    for imageUrl in imageUrls:
        urlToImage(imageUrl, basePath, """展示图{}.png""".format(count))
        time.sleep(0.5)
        count += 1


def any_elements_exists(driver: WebBotMain, xpathList, stringInclude, tryTimes=5):
    """
    找到元素，并且滚动页面到页面附近,通过元素内含文字判断元素是否存在
    :param driver:
    :param xpathList:
    :param tryTimes:
    :return:
    """
    driver.scroll_mouse(0, -9999)  # 首先滚动到最顶部
    time.sleep(0.5)
    for tryTime in range(tryTimes):
        for xpath in xpathList:
            text = driver.get_element_text(xpath)
            if text != None and stringInclude in text:
                return xpath
        driver.scroll_mouse(0, 500)
        time.sleep(0.5)
    return None


def getAllImage(driver: WebBotMain, basePath):
    # 主界面截图
    saveImage(driver, basePath, "主图.png")
    print("截图完成..")
    # 展示的几张图片
    saveShowImage(driver, basePath)
    print("抓取展示图片完成..")
    try:
        # 进入查看全部信息，有的商品会有
        btnXpath = any_elements_exists(driver, btnXpathList, "全部信息", tryTimes=2)
        a = driver.get_element_rect(btnXpath)
        driver.click_mouse((a[0][0] + 5, a[0][1] + 5), 1)
    except:
        a = 1
    # 店铺名
    # driver.scroll_mouse(0, 1000)
    time.sleep(0.2)
    shopNameXpath = any_elements_exists(driver, shopNameXpathList, "\n")
    shopName = driver.get_element_text(shopNameXpath)
    shopName = shopName.split('\n')[0]
    print("店铺名：", shopName)
    # 参数详情
    driver.scroll_mouse(0, -9999)
    time.sleep(0.2)
    infoXpath = any_elements_exists(driver, infoXpathList, "参数")
    position = driver.get_element_rect(infoXpath)
    driver.scroll_mouse(0, position[0][1])
    time.sleep(0.5)
    saveImage(driver, basePath, "参数.png")
    print("完成...")
    return shopName


def main(driver: WebBotMain):
    #     urls = """https://v.douyin.com/SGf7W3p/
    # https://v.douyin.com/StG78EC/
    # https://v.douyin.com/SGf7W3p/
    # https://v.douyin.com/StGwAx9/
    # https://v.douyin.com/StGqdQW/
    # https://v.douyin.com/StGGHGQ/"""
    #     urls = urls.split('\n')
    #     jsScript = """<script>
    # window.moveTo(0,   0);//移动窗口
    # window.resizeTo(500,   900);//改变大小
    # window.onresize=new   Function("window.resizeTo(500,   900);")
    # </script>"""
    #     url = "https://v.douyin.com/StGwAx9/"
    #     driver.execute_script(jsScript)
    maxRow = sheet.max_row
    maxCol = sheet.max_column
    result = getAllData(sheet)
    for rowID in range(2, maxRow + 1):
        waitTimeBase = 0
        if readXlsx(sheet, row=rowID, col=maxCol - 2) == "是":
            continue
        url = readXlsx(sheet, row=rowID, col=1)
        ##############################################
        # 判断是否重复爬虫
        if url in result.keys():  # 数据已经存在
            temp = result[url]
            writeXlsx(sheet, row=rowID, col=maxCol - 2, value=temp[0])
            writeXlsx(sheet, row=rowID, col=maxCol - 1, value=temp[1])
            writeXlsx(sheet, row=rowID, col=maxCol - 0, value=temp[2])
            try:
                wb.save(xlsxPath)
            except:
                a = 1
            continue
        ##############################################
        # 没有存储此条数据，开始爬虫
        result[url] = [None, None, None]
        print("开始...", url)
        path = os.path.join('data/temp', removeSpecialChar(string=url))
        createFold(path)
        driver.goto(url)
        time.sleep(float(config['asd']['waitTimeAfterGoto']))
        # 1 获取店铺名和截取图片
        shopNAme = ""
        try:
            waitTimeBase = 1
            shopNAme = getAllImage(driver, path)
            result[url][0] = "是"
            result[url][1] = shopNAme
        except:
            result[url][0] = "失败"
            a = 1
            print("失败：", url)
        # 2 将图片拼合并转化成PDF
        try:
            waitTimeBase = 1
            png2png(path, 3)
            pdfPath = png2PDF(path, "{}违规证明".format(shopNAme))
            result[url][2] = pdfPath
        except:
            a = 1
        # 3 删除包含png的文件
        if config['asd']['removeImage'] == "1":
            delFileContainX(path, 'png')
        # 4 写入表格
        for num in range(len(result[url])):
            writeXlsx(sheet, row=rowID, col=maxCol - 2 + num, value=result[url][num])
        # 5 保存表格
        try:
            wb.save(xlsxPath)
        except:
            a = 1
        # 每爬取一条信息之后的等待时间
        time.sleep(float(config['asd']['waitTimePerUrl']) * waitTimeBase)


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
