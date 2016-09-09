# -*- coding: cp936 -*-
import re
def prefunc(debugFilePath):

    ###打开并按行读取debug dp snoop-len信息-->###
    snoopLenFile = open(debugFilePath,'r',0)
    snoopLenLines = snoopLenFile.readlines()
    lenOfAll = len(snoopLenLines)#l1表示整个文件的行数
    token = '------------------------------------------------\n'#提取snooplen信息时的参照标记
    ###<--打开并按行读取debug dp snoop-len信息###



    ###获取debug报文的时间戳列表及所在行数的列表-->###
    timeList = []
    lineOfTime = []
    for i in range(lenOfAll):
        tmp = re.findall(r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)',snoopLenLines[i])
        if len(tmp) == 1:
            timeList.append(tmp[0])
            lineOfTime.append(i)
    ###<--获取debug报文的时间戳列表###


    num = len(timeList)#num1表示报文的数量，和时间戳的数量一致


    ###获取debug报文的十六进制码列表-->###
    frameList = num * ['']
    snooplenTmpList = (num-1) * [[]]
    for i in range(num-1):
        snooplenTmpList[i] = snoopLenLines[lineOfTime[i]:lineOfTime[i+1]]
    snooplenTmpList.append(snoopLenLines[lineOfTime[num-1]:])

    for i in range(num):
        snooplentmp = snooplenTmpList[i][snooplenTmpList[i].index(token)+1:]
        x = 0
        while True:
            if snooplentmp[x] != token:
                frameList[i] += snooplentmp[x]
                x += 1
            else:
                break

    for i in range(num):
        frameList[i] = frameList[i].replace('\n','').replace(' ','')
    ###<--获取debug报文的十六进制码列表###

    return {'num':num,'timeList':timeList,'frameList':frameList}
