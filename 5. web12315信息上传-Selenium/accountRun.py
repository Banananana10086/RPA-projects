import os
import time

from driverOperation import xpath, login, isLoginSuccess, driverInit, logout
from fileOperation import copyFold, createFold, rmdir
from web12315Operation import runPerData


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                       time_tuple[5])


def isNameInList(name, path):
    foldNames = os.listdir(path)
    for foldName in foldNames:
        if name in foldName:
            return True
    return False


def runPerAccount(nameAndAccount):
    createFold(r"D:/temp")
    createFold(r"data/失败")
    # waitTime = int(input("完成一个之后的等待时间（秒）"))
    waitTime = 1
    driver = driverInit()
    for name in nameAndAccount:
        if isNameInList(name, "data/数据"):  # 如果该账号在列表中有数据
            account = nameAndAccount[name][0]
            password = nameAndAccount[name][1]
            people = name
            # 登录操作
            login(driver, account, password)
            tryTimes = 0
            while not isLoginSuccess(driver):
                tryTimes += 1
                if tryTimes >= 4:
                    print("登录失败...", account, password, people)
                    return
                login(driver, account, password)
            print("---", people)

            if len(os.listdir("./data/数据")) != 0:
                folds = os.listdir("./data/数据".format(people))
                count = 0  # 统计该账号提交了多少条信息
                for fold in folds:
                    if count == 10:  # 提交够十个就退出循环
                        break
                    if name in fold:
                        print("---", people, "---", fold)
                        sourcePath = r'./data/数据/{}'.format(fold)
                        targetPath = r'./data/失败/{}'.format(fold)
                        txtName = ""
                        for i in os.listdir(sourcePath):
                            if '.txt' in i:
                                txtName = i
                        if txtName == "":
                            # print("该目录下没有.txt文件")
                            createFold(r'./data/失败/{}'.format(fold))
                            createFold(r'./data/失败/{}'.format(fold))
                            print("--- 失败 ---", people, fold, "目录下没有txt文本")
                            copyFold(sourcePath, targetPath)
                            rmdir(sourcePath)
                            continue
                        try:
                            runPerData(driver, os.path.join(sourcePath, txtName))
                            print("--- 成功 ---", people, fold)
                            count += 1  # 提交成功就加一条
                            createFold(r'./data/成功')
                            createFold(r'./data/成功/{}'.format(fold))
                            copyFold(sourcePath, r'./data/成功/{}'.format(fold))
                            rmdir(sourcePath)
                        except:
                            print("--- 失败 ---", people, fold)
                            createFold(r'./data/失败')
                            createFold(r'./data/失败/{}'.format(fold))
                            copyFold(sourcePath, targetPath)
                            rmdir(sourcePath)
                            # 输出错误信息
                            try:
                                error = xpath(driver, """//*[@id="alertspan"]""").text
                                errorPath = targetPath + "/{}".format(error)
                                open(errorPath, 'w')
                                print("*** 错误信息：", error)
                                
                                count = 10  # 超过今日限额
                            except:
                                a = 1

                        time.sleep(waitTime)
            print(account, people, "结束")
            print(getCurrentTime())
            print("-------------- 正在切换账号...")
            logout(driver)  # 退出登录
            time.sleep(10)
            # if len(os.listdir(r".\data\数据\{}".format(people))) == 0:
            #     rmdir(r".\data\数据\{}".format(people))
