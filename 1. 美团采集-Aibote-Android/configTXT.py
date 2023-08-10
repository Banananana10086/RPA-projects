def TxtToDict(txtPath, seq="："):
    f = open(txtPath, encoding='utf-8')
    temp = f.readlines()
    f.close()
    lines = []
    for i in temp:
        if i != '' or i != '\n':
            lines.append(i.replace('\n', ''))
    result = {}
    for line in lines:
        try:
            temp = line.split(seq)
            result[temp[0]] = temp[1]
        except:
            a = None
    return result


if __name__ == "__main__":
    txtPath = r"./data/配置文件.txt"
    config = TxtToDict(txtPath, seq="：")
    print(config)
