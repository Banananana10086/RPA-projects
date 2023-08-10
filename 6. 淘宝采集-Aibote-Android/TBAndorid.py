# 1. 导入 AndroidBotMain 类
import re

from AiBot import AndroidBotMain
import time
from config import config
from fileOperation import *

driverBasePath = r"/storage/emulated/0/Android/data/com.aibot.client/files/"  # aiBote存储图片默认路径
createFold(r'./data/temp')


# 2. 自定义一个脚本类，继承 AndroidBotMain
class CustomAndroidScript(AndroidBotMain):
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
        # 6.1 API 演示
        # 注意：Python 版本支持的 Api 与 Nodejs 基本相同
        # 教程中仅演示部分 Api，更多 Api 请自行探索，所有 Api 均包含详细的参数要求和返回值，请自行查看。

        # 截图
        main(self)


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                             time_tuple[5])
    # return "{}年{}月{}日{}点{}分".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4])


def slide(driver: CustomAndroidScript, num, duration=0.2):
    """
    正数为向下滑动\n
    :param driver:
    :param num:
    :param duration:
    :return:
    """
    windowSize = driver.get_window_size()
    driver.swipe(start_point=(windowSize['width'] / 2, windowSize['height'] / 2),
                 end_point=(windowSize['width'] / 2, windowSize['height'] / 2 - num), duration=duration)
    time.sleep(duration + 0.2)


def getItemName(driver: CustomAndroidScript):
    itemNameXpathList = [
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[1]/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[2]/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[3]/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[4]/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[5]/android.widget.TextView"""]
    temp = None
    for itemNameXpath in itemNameXpathList:
        temp = driver.get_element_text(itemNameXpath, wait_time=0.5)
        # print(temp)
        if "商品券满" not in str(temp) and "淘金币可抵" not in str(temp) and "购买得积分" not in str(
                temp) and "月销" not in str(temp) and str(
            temp) != "None":
            break
    # print(temp)
    itemName = re.findall(r'[\u4e00-\u9fa5]', temp)  # 提取其中的所有汉字
    itemName = "".join(itemName)
    # print(itemName)
    return itemName


def getShopName(driver: CustomAndroidScript, tryTimes=5):
    shopNameXpathList = [
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[3]/android.widget.FrameLayout/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[5]/android.widget.FrameLayout/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[6]/android.widget.FrameLayout/android.widget.TextView""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.View""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/android.view.View""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[4]/android.widget.FrameLayout[1]/android.view.View""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[5]/android.widget.FrameLayout[1]/android.view.View""",
        """com.taobao.taobao/com.taobao.taobao:id=mainpage2/android.widget.FrameLayout[6]/android.widget.FrameLayout[1]/android.view.View"""
    ]
    shopName = ""
    for count in range(tryTimes):
        for shopNameXpath in shopNameXpathList:
            temp = driver.get_element_text(xpath=shopNameXpath, wait_time=0.1)
            if temp == None:
                temp = driver.get_element_desc(xpath=shopNameXpath, wait_time=0.1)
            temp = str(temp)
            print(temp)
            if temp != "None" and "推荐" not in temp:
                shopName = temp
                break
        if shopName != "":
            break
        slide(driver, 500)
    print(shopName)
    return shopName


def tbUrl2Message(driver: CustomAndroidScript, url):
    # 输入url并进入
    print(url.strip())
    while not driver.set_element_text(text=url.strip(),
                                      xpath="""com.taobao.taobao/com.taobao.taobao:id=searchEdit""", wait_time=2):
        driver.back()
    driver.click_element(xpath="""com.taobao.taobao/com.taobao.taobao:id=searchbtn""")
    time.sleep(float(config['asd']["waitTimeOfPageLoading"]))  # 等待页面加载完成
    ########################################
    # 1 --- 提取信息 - 商品名
    if int(config['asd']['getItemName']) == 1:
        slide(driver, 500, 0.5)
        itemName = getItemName(driver)
        slide(driver, -500, 0.5)
    else:
        itemName = "某商品"
    # 2 --- 创建对应资源文件夹
    dataPath = r'./data/temp/{}-{}'.format(removeSpecialChar(itemName.strip()), getCurrentTime())
    createFold(dataPath)
    # 3 --- 提取信息 - 主页面
    driver.save_screenshot(image_name="主图.png")
    driver.pull_file(remote_path=driverBasePath + "主图.png", local_path=os.path.join(dataPath, "主图.png"))
    # 4 --- 提取信息 - 展示图片
    # 定位图片
    pictureXpathList = ["""com.taobao.taobao/com.taobao.taobao:id=picGalleryVideoPlayerCustomizeContainer""",
                        """com.taobao.taobao/com.taobao.taobao:id=standard_detail_gallery_id_frame_content""",
                        """com.taobao.taobao/com.taobao.taobao:id=frame_float_layout"""]
    pictureXpath = driver.any_elements_exists(pictureXpathList, wait_time=0.2, interval_time=0.2)
    imagePos = driver.get_element_rect(xpath=pictureXpath)  # 截图坐标点
    # 获取图片
    try:
        # 方法1
        pictureNum = driver.get_element_text(xpath="""com.taobao.taobao/com.taobao.taobao:id=mainpic_text_indicator""",
                                             wait_time=0.5)
        pictureNum = int(pictureNum.split('/')[-1])
        print("共有{}张图片".format(pictureNum))
        for i in range(pictureNum):
            imName = "展示图片{}.png".format(i + 1)
            driver.save_screenshot(image_name=imName,
                                   region=(imagePos[0][0], imagePos[0][1], imagePos[1][0], imagePos[1][1]))
            driver.pull_file(remote_path=driverBasePath + imName, local_path=os.path.join(dataPath, imName))
            if i + 1 != pictureNum:  # 最后一次循环不进行滑动
                imPosCenter = ((imagePos[0][0] + imagePos[1][0]) / 2, (imagePos[0][1] + imagePos[1][1]) / 2)
                driver.swipe(start_point=(imPosCenter[0] * 2 - 1, imPosCenter[1]), end_point=(0, imPosCenter[1]),
                             duration=0.3)
                time.sleep(0.7)
    except:
        # 方法2
        num = 1
        pictureXpath = """com.taobao.taobao/com.taobao.taobao:id=standard_detail_gallery_id_frame_content"""
        while True:
            if not driver.element_exists(xpath=pictureXpath, wait_time=1):
                break
            imName = "展示图片{}.png".format(num)
            driver.save_screenshot(image_name=imName,
                                   region=(imagePos[0][0], imagePos[0][1], imagePos[1][0], imagePos[1][1]))
            driver.pull_file(remote_path=driverBasePath + imName, local_path=os.path.join(dataPath, imName))
            imPosCenter = ((imagePos[0][0] + imagePos[1][0]) / 2, (imagePos[0][1] + imagePos[1][1]) / 2)
            driver.swipe(start_point=(imPosCenter[0] * 2 - 1, imPosCenter[1]), end_point=(0, imPosCenter[1]),
                         duration=0.3)
            time.sleep(1)
            num += 1
        while not driver.element_exists(xpath=pictureXpath, wait_time=1):
            driver.back()

    # 5 --- 提取信息 - 详情页面
    # 进入详情页面
    # windowSize = driver.get_window_size()
    infoPos = []
    count = 0
    while infoPos == [] and count <= 5:
        count += 1
        slide(driver, 800, 0.5)
        time.sleep(1)
        infoPos = driver.find_images("参数1.png", similarity=float(config['asd']['sim1']))  # 找图坐标
        if infoPos == []:
            infoPos = driver.find_images("参数.png", similarity=float(config['asd']['sim2']))
    driver.click(infoPos[0])
    time.sleep(1)
    # 截取详情1
    driver.save_screenshot(image_name="详情1.png")
    driver.pull_file(remote_path=driverBasePath + "详情1.png", local_path=os.path.join(dataPath, "详情1.png"))
    # 向下滑动
    slide(driver, 500)
    # 截取详情2
    slide(driver, 800)
    driver.save_screenshot(image_name="详情2.png")
    driver.pull_file(remote_path=driverBasePath + "详情2.png", local_path=os.path.join(dataPath, "详情2.png"))
    driver.back()
    time.sleep(1)
    # 6 --- 提取信息 - 店铺名
    slide(driver, 500)
    if int(config['asd']['getShopName']) == 1:
        shopName = getShopName(driver)
    else:
        shopName = "店铺"
    ########################################
    # 文件操作 - 合并图像
    # 返回搜索框，以便进行下一条url操作
    png2png(dataPath, 3)
    pdfPath = png2PDF(dataPath, "{}违规证明".format(shopName))
    driver.back()
    time.sleep(2)
    return ["是", shopName, pdfPath]


def main(driver: CustomAndroidScript):
    # 初始化操作
    driver.wait_timeout = 3
    driver.push_file(r"./data/imageSource/参数.png", driverBasePath + "参数.png")
    driver.push_file(r"./data/imageSource/参数.png", driverBasePath + "参数1.png")
    # 启动淘宝
    driver.start_app("淘宝")
    # 进入淘宝搜索框
    driver.click((504, 170))
    time.sleep(1)
    from xlsxOperation import XLSX, exchange
    xlsxPath = exchange('./data')
    xlsxPath = './data/{}'.format(xlsxPath)
    xlsx = XLSX(path=xlsxPath, headList=["是否完成爬虫", "店铺名", "PDF路径"])
    count = 1
    while True:
        print("---------", count, "---------")
        count += 1
        # 提取url
        try:
            url = xlsx.getUrl()
        except IndexError:
            break
        # 爬虫
        try:
            data = tbUrl2Message(driver, url)
            xlsx.writeUrlAndData(url, data)
        except:
            print("""-----该条链接处理失败：{}""".format(url))
            xlsx.writeUrlAndData(url, ["失败", None, None])
    print("所有信息处理完成....")
    time.sleep(9999)


# 7. 执行脚本，Pycharm 中，直接右键执行
if __name__ == '__main__':
    # 注意：此处监听的端口号，必须和手机端的脚本端口号一致；
    # 监听 3333 号端口
    CustomAndroidScript.execute(16678)
