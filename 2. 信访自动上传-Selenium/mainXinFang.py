import time

from driverOperation import *
from fileOperation import *
from webOperation import *


def initMain():
    createFold("./data/已完成")
    createFold("./data/上传失败")


def readAccount(accountPath):
    """
    从目录下的一个txt文本中获取文件信息，文本中信息格式为
    谭龙刚/43112120020912101X/w1998523/2022/06/16/2032/06/16\n
    :param accountPath:
    :return:
    """
    txtNames = findFilesBasisSuffix(accountPath, "txt")
    account = {}  # 用户信息字典
    if len(txtNames) == 0:
        print("账号文件夹中没有填入账号")
        time.sleep(9999)
    else:
        txtPath = accountPath + '/' + txtNames[-1]
        f = open(txtPath, encoding='utf-8')
        string = f.readlines()
        f.close()
        newString = []
        for stringTemp in string:
            if removeSpecialCharLess(stringTemp) != "":
                newString.append(removeSpecialCharLess(stringTemp))
        for perMessage in newString:
            exceptName = []
            perMessage = perMessage.split('/')
            exceptName.append(perMessage[1])  # 身份证号码
            exceptName.append(perMessage[2])  # 密码
            exceptName.append(('/').join(perMessage[3:6]))  # 有效期开始
            exceptName.append(('/').join(perMessage[6:9]))  # 有效期结束
            account[perMessage[0]] = exceptName
    return account


def data(driver, dataPath, account):
    """
    在data文件夹中的操作\n
    :param driver:
    :param dataPath:
    :param account:
    :return:
    """
    foldList = os.listdir(dataPath)
    nameAndTxt = {}
    for fold in foldList:
        txtName = findFilesBasisSuffix(dataPath + '/' + fold, 'txt')
        txtName = txtName[-1]
        txtPath = dataPath + '/' + fold + '/' + txtName
        name = txtName.split("【")[1].split("】")[0]  # 从文件夹名称中提取出姓名
        nameAndTxt[name] = txtPath
    for name in nameAndTxt:
        print("---------------------------------------------")
        try:
            temp = account[name]
        except:
            print("没有 {} 的账号密码等信息".format(name))
            continue
        print("--- 开始处理.. {}  {}".format(name, nameAndTxt[name]))
        sourcePath = r"./data/未完成/{}"
        targetPath = r'./data/已完成/{}'
        targetPath2 = r'./data/上传失败/{}'
        try:
            flag = perAccount(driver, name, account[name], nameAndTxt[name])
            foldName = nameAndTxt[name].split("/")[-2]
            if flag:  # 没有出现上传失败情况
                copyFold(sourcePath.format(foldName), targetPath.format(foldName))
                rmdir(sourcePath.format(foldName))
            else:  # 出现上传失败情况
                copyFold(sourcePath.format(foldName), targetPath2.format(foldName))
                rmdir(sourcePath.format(foldName))
        except:  # 失败
            a = 1
        # 退出登录
        try:
            logout(driver)
        except:
            a = 1


if __name__ == "__main__":
    driver = driverInit()
    initMain()
    accountPath = r"./账号"
    account = readAccount(accountPath)
    dataPath = r"./data/未完成"
    data(driver, dataPath, account)
    print("结束...")
    time.sleep(99999)
