import os
import shutil


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


def findFilesBasisSuffix(path, suffix):
    """
    找出path目录下，suffix后缀的文件，形成列表，列表第一个文件元素为“”
    :param path: 目录
    :param suffix: 文件内后缀
    :return: 列表
    """
    fileName = []
    for i in os.listdir(path):
        if suffix in i:
            fileName.append(i)
    return fileName


def createFold(path):
    try:
        os.mkdir(path)
    except:
        a = 1


def rmdir(dir):
    # 判断是否是文件夹，如果是，递归调用rmdir()函数
    if os.path.isdir(dir):
        # 遍历地址下的所有文件及文件夹
        for file in os.listdir(dir):
            # 进入下一个文件夹中进行删除
            rmdir(os.path.join(dir, file))
        # 如果是空文件夹，直接删除
        if os.path.exists(dir):
            os.rmdir(dir)
    # 如果是文件，直接删除
    else:
        if os.path.exists(dir):
            os.remove(dir)


def copyFold(path, target):
    if os.path.exists(target):
        rmdir(target)
    os.mkdir(target)
    for ipath in os.listdir(path):
        fullDir = os.path.join(path, ipath)  # 拼接成绝对路径
        if os.path.isfile(fullDir):  # 文件，匹配->打印
            shutil.copy(fullDir, target)
