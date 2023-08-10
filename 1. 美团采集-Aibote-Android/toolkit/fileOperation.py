import os
import shutil

import img2pdf
from PIL import Image
import os


def removeSpecialCharV1(temp):
    """
    删除换行和制表符\n
    :param temp:
    :return:
    """
    temp = temp.replace("""\n""", '')
    temp = temp.replace("""\t""", '')
    temp = temp.replace(""" """, '')
    return temp


def removeSpecialCharV2(temp):  # 删除特殊字符
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
    temp = temp.replace("""$""", '')
    temp = temp.replace("""&""", '')
    temp = temp.replace(""".""", '')
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


def rmdir(fold):
    # 判断是否是文件夹，如果是，递归调用rmdir()函数
    if os.path.isdir(fold):
        # 遍历地址下的所有文件及文件夹
        for file in os.listdir(fold):
            # 进入下一个文件夹中进行删除
            rmdir(os.path.join(fold, file))
        # 如果是空文件夹，直接删除
        if os.path.exists(fold):
            os.rmdir(fold)
    # 如果是文件，直接删除
    else:
        if os.path.exists(fold):
            os.remove(fold)


def copyFold(path, target):
    if os.path.exists(target):
        rmdir(target)
    os.mkdir(target)
    for ipath in os.listdir(path):
        fullDir = os.path.join(path, ipath)  # 拼接成绝对路径
        if os.path.isfile(fullDir):  # 文件，匹配->打印
            shutil.copy(fullDir, target)


def removeSpecialChar(string: str):
    string = string.replace("""<""", "")
    string = string.replace(""">""", "")
    string = string.replace(""":""", "")
    string = string.replace("""/""", "")
    string = string.replace("""\\""", "")
    string = string.replace("""?""", "")
    string = string.replace("""*""", "")
    string = string.replace("""|""", "")
    string = string.replace('"', "")
    string = string.replace("'", "")
    string = string.replace(".", "")
    return string


def png2png(basePath, num):
    """
    将temp中的png图片拼合\n
    :param basePath: 路径
    :param num: 一行显示多少个展示图片
    :return:
    """
    # 获取图片列表
    img1 = Image.open(r'{}/主图.png'.format(basePath))
    img2 = Image.open(r'{}/参数.png'.format(basePath))
    img3 = Image.open(r'{}/展示图1.png'.format(basePath))
    img3List = []
    i = 1
    while True:
        if os.path.exists(r'{}/展示图{}.png'.format(basePath, i)):
            img3List.append(r'{}/展示图{}.png'.format(basePath, i))
        else:
            break
        i += 1
    img1Size = img1.size
    img2Size = img1.size
    img3Size = list(img3.size)
    for temp in img3List:
        img = Image.open(temp)
        img3Size[0] = max([img3Size[0], img.size[0]])
        img3Size[1] = max([img3Size[1], img.size[1]])

    # 生成新图片
    newPNG = Image.new("RGB",
                       (max([img1Size[0], img2Size[0], img3Size[0] * num]),
                        img1Size[1] + img2Size[1] + (int(len(img3List) / num) + 1) * img3Size[1]),
                       color='white')
    newPNG.paste(img1, (0, 0))
    newPNG.paste(img2, (0, img1Size[1]))
    start = img1Size[1] + img2Size[1]
    for i in range(len(img3List)):
        width = i % num
        length = int(i / num)
        img30 = Image.open(img3List[i])
        newPNG.paste(img30, (width * img3Size[0], start + length * img3Size[1]))
        img30.close()
    newPNG.save("{}/总图.png".format(basePath))
    img1.close()
    img2.close()
    img3.close()


def png2PDF(basePath, pdfName):
    """
    将图片转化为PDF
    :param basePath: 路径
    :param pdfName:要保存为的pdf文件名
    :return:
    """
    with open("{}/{}.pdf".format(basePath, pdfName), "wb") as file:
        file.write(img2pdf.convert(os.path.join(basePath, "总图.png")))
        file.close()
    return os.path.abspath("{}/{}.pdf".format(basePath, pdfName))


def delFileContainX(path, X):
    fileList = os.listdir(path)
    for file in fileList:
        if X in file:
            os.remove(os.path.join(path, file))


def loadXpath(textPath):
    f = open(textPath, encoding='utf-8')
    temp = f.readlines()
    f.close()
    xpathList = []
    for i in temp:
        if i != '' or i != '\n':
            xpathList.append(i.replace('\n', ''))
    return xpathList


def listToTxt(data: list, txtFile):
    """
    把列表写入txt文件
    :param data:
    :param txtFile:
    :return:
    """
    f = open(txtFile, 'w', encoding='utf-8')
    f.writelines('\n'.join(data))
    f.close()


def shopImageMerge(sourcePath, companyName):
    """
    合并 "店铺展示页.png" 和 "医师资审核.png"
    :param companyName: 公司名
    :param sourcePath:
    :return: PDF绝对路径
    """
    # 合并图像
    img1 = Image.open(os.path.join(sourcePath, "店铺展示页.png"))
    img2 = Image.open(os.path.join(sourcePath, "医师资格审核.png"))
    img1Size = img1.size
    img2Size = img1.size
    newPNG = Image.new("RGB",
                       (img1Size[0] * 2, img1Size[1]),
                       color='white')
    newPNG.paste(img1, (0, 0))
    newPNG.paste(img2, (img1Size[0], 0))
    newPNG.save(os.path.join(sourcePath, "总图.png"))
    img1.close()
    img2.close()
    # 转化PDF
    return png2PDF(sourcePath, "{}发布违法广告证据".format(companyName))


def itemImageMerge(sourcePath, shopName):
    """
    合并 “商品主页面.png”， “套餐详情.png”， “商品图文介绍1.png”最多到6
    :param sourcePath:
    :param shopName:
    :return: pdf绝对路径
    """
    img1 = Image.open(os.path.join(sourcePath, "商品主页面.png"))
    img2 = Image.open(os.path.join(sourcePath, "套餐详情.png"))
    img3 = Image.open(os.path.join(sourcePath, "商品图文介绍1.png"))
    img3List = []
    count = 1
    while True:
        if os.path.exists(os.path.join(sourcePath, "商品图文介绍{}.png".format(count))):
            img3List.append(os.path.join(sourcePath, "商品图文介绍{}.png".format(count)))
        else:
            break
        count += 1
    img1Size = img1.size
    img2Size = img2.size
    img3Size = img3.size
    # 生成新图片
    newPNG = Image.new("RGB",
                       (img1Size[0] * 3,
                        img1Size[1] * 3),
                       color='white')
    newPNG.paste(img1, (0, 0))
    newPNG.paste(img2, (img1Size[0], 0))
    start = img1Size[1]
    num = 3
    for i in range(len(img3List)):
        width = i % num
        length = int(i / num)
        img30 = Image.open(img3List[i])
        newPNG.paste(img30, (width * img3Size[0], start + length * img3Size[1]))
        img30.close()
    newPNG.save(os.path.join(sourcePath, "总图.png"))
    img1.close()
    img2.close()
    img3.close()
    # 生成PDF
    return png2PDF(sourcePath, "{}其他产品违法广告".format(shopName))


if __name__ == "__main__":
    # sourcePath = r"""C:\Users\31745\PycharmProjects\pythonProject\爬虫\美团\data\temp\httpdpurlcnBgxkzTpz"""
    # pdfPath = itemImageMerge(sourcePath, "某商店")
    # print(pdfPath)
    print("helloWord")
