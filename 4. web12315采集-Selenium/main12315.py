import os
import time

import openpyxl as op

from driverOperation import *
from perAccount import perAccount, removeSpecialChar, removeSpecialCharLess


def createFold(path):
    try:
        os.mkdir(path)
    except:
        a = 1


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    # return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
    #                                    time_tuple[5])
    return "{}年{}月{}日{}点{}分".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4])


def initMain():
    pdfPath = "./data/" + getCurrentTime() + "-PDF"
    createFold(pdfPath)
    return os.path.abspath(pdfPath)


def tryDistGet(distA, key):
    value = ""
    try:
        return distA[key]
    except:
        return " "


def getAccountAndPassword(filePath):
    fileName = []
    for i in os.listdir(filePath):
        if ".txt" in i:
            fileName.append(i)
    fileName = fileName[0]
    fileName = filePath + '/' + fileName
    al = []
    pl = []
    f = open(fileName, encoding='utf-8')
    string = f.readlines()
    f.close()
    new = []
    for i in string:
        if i != '\n':
            new.append(i)
    for i in new:
        temp = i.strip().split(" ")
        al.append(temp[0])
        pl.append(temp[1])
    return al, pl


def run(pdfPath):
    time.sleep(5)
    print("-----------------------------------")
    year = input("信息日期设定\n输入年份(例: 2023)")
    month = input("输入月份(例: 2)")
    day = input("输入日期(例: 19)")
    al, pl = getAccountAndPassword(r"./账号")
    excelPath = "./data/{}年{}月{}日--提取日期：".format(year, month, day) + getCurrentTime() + ".xlsx"
    print(excelPath)
    wb = op.Workbook()
    ws = wb['Sheet']  # 创建子表
    ws.append(['名字', '编号', '经营者', '商品名称', '状态', '开始日期', '附件', '结束日期', '订单号', '处理单位', '处理单位具体', '原因', '举报内容', ])
    for accountNum in range(len(al)):
        account = al[accountNum]
        password = pl[accountNum]
        data = perAccount(driver, account, password, [year, month, day])
        for perDist in data:
            for key in perDist:
                perDist[key] = removeSpecialCharLess(perDist[key])
        for perDist in data:
            temp = [
                perDist['name'],  # 名字
                perDist['number'],  # 编号
                perDist['operator'],  # 经营者
                perDist['item'],  # 商品名称
                perDist['status'],  # 状态
                perDist['date'],  # 开始日期
            ]
            if perDist["status"] == '不予立案' or perDist['status'] == '处理完成':
                hyperLink = """=HYPERLINK("{}", "PDF")"""
                hl = hyperLink.format(pdfPath + "\\" + perDist['number'] + '.pdf')
                temp.append(hl)  # 附件
                # 结束日期
                if perDist['status'] == '不予立案':
                    temp.append(perDist['告知时间'])
                elif perDist['status'] == '处理完成':
                    temp.append(perDist['反馈时间'])
                # 订单号
                temp.append(tryDistGet(perDist, "订单号"))
                # 处理单位
                temp.append(tryDistGet(perDist, "处理单位"))
                # 处理单位具体
                temp.append(tryDistGet(perDist, "处理单位具体"))
                # 原因
                if perDist['status'] == '不予立案':
                    temp.append(removeSpecialCharLess(tryDistGet(perDist, "不立案原因")))
                elif perDist['status'] == '处理完成':
                    temp.append(removeSpecialCharLess(tryDistGet(perDist, "反馈内容")))
                # 举报内容
                temp.append(removeSpecialCharLess(tryDistGet(perDist, "举报内容")))
            print("----------------------------")
            print(temp)
            ws.append(temp)
            time.sleep(0.5)
        wb.save(excelPath)  # 异步操作
        time.sleep(3)
        # 退出当前账号
        exitAccount(driver)


if __name__ == '__main__':
    # print(time.time())
    # if time.time() < 1676943024.169657:
    pdfPath = initMain()
    driver = driverInit(pdfPath)
    run(pdfPath)
    print("结束.....")
    time.sleep(9999)
