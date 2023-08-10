import os
import shutil

import img2pdf
from PIL import Image


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


def createFold(path):
    try:
        os.mkdir(path)
    except:
        a = 1


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
    img21 = Image.open(r'{}/详情1.png'.format(basePath))
    img22 = Image.open(r'{}/详情2.png'.format(basePath))
    img3 = Image.open(r'{}/展示图片1.png'.format(basePath))
    img3List = []
    i = 1
    while True:
        if os.path.exists(r'{}/展示图片{}.png'.format(basePath, i)):
            img3List.append(r'{}/展示图片{}.png'.format(basePath, i))
        else:
            break
        i += 1
    img1Size = img1.size
    img2Size = img21.size
    img3Size = list(img3.size)
    for temp in img3List:
        img = Image.open(temp)
        img3Size[0] = max([img3Size[0], img.size[0]])
        img3Size[1] = max([img3Size[1], img.size[1]])

    # 生成新图片
    newPNG = Image.new("RGB",
                       (max([3 * img1Size[0], 3 * img3Size[0]]),
                        img1Size[1] + (int(len(img3List) / num) + 1) * img3Size[1]),
                       color='white')
    newPNG.paste(img1, (0, 0))
    newPNG.paste(img21, (img1Size[0], 0))
    newPNG.paste(img22, (img1Size[0] * 2, 0))
    start = img1Size[1]
    for i in range(len(img3List)):
        width = i % num
        length = int(i / num)
        img30 = Image.open(img3List[i])
        newPNG.paste(img30, (width * img3Size[0], start + length * img3Size[1]))
        img30.close()
    newPNG.save("{}/总图.png".format(basePath))
    img1.close()
    img21.close()
    img22.close()
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


if __name__ == "__main__":
    import os

    path = r"/web信息爬取/aibote/DY/data/temp/httpsvdouyincomStG78EC"
    num = 3
    png2png(path, num)
