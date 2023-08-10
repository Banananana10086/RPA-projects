import os
import time

from driverOperation import driverInit
from fileOperation import getAccountAndPassword, findFilesBasisSuffix, createFold
from accountRun import runPerAccount

createFold("D:/temp")


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                       time_tuple[5])


if __name__ == '__main__':
    # if time.time() < 1676094438:
    accountFilePath = r'.\账号'
    txtName = findFilesBasisSuffix(accountFilePath, ".txt")
    accountList, passwordList, nameList = getAccountAndPassword(os.path.join(accountFilePath, txtName[-1]))
    nameAndAccount = {}
    # 生成名字对应的账号字典
    for i in range(len(accountList)):
        nameAndAccount[nameList[i]] = [accountList[i], passwordList[i]]
    print(accountList, passwordList, nameList)
    runPerAccount(nameAndAccount)
    print("处理完成...")
    time.sleep(99999)
