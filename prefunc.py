# -*- coding: cp936 -*-
import re
def prefunc(debugFilePath):

    ###�򿪲����ж�ȡdebug dp snoop-len��Ϣ-->###
    snoopLenFile = open(debugFilePath,'r',0)
    snoopLenLines = snoopLenFile.readlines()
    lenOfAll = len(snoopLenLines)#l1��ʾ�����ļ�������
    token = '------------------------------------------------\n'#��ȡsnooplen��Ϣʱ�Ĳ��ձ��
    ###<--�򿪲����ж�ȡdebug dp snoop-len��Ϣ###



    ###��ȡdebug���ĵ�ʱ����б������������б�-->###
    timeList = []
    lineOfTime = []
    for i in range(lenOfAll):
        tmp = re.findall(r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)',snoopLenLines[i])
        if len(tmp) == 1:
            timeList.append(tmp[0])
            lineOfTime.append(i)
    ###<--��ȡdebug���ĵ�ʱ����б�###


    num = len(timeList)#num1��ʾ���ĵ���������ʱ���������һ��


    ###��ȡdebug���ĵ�ʮ���������б�-->###
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
    ###<--��ȡdebug���ĵ�ʮ���������б�###

    return {'num':num,'timeList':timeList,'frameList':frameList}
