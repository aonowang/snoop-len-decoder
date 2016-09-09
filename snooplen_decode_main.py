# -*- coding: cp936 -*-
import re

from tables import *
from prefunc import *
from classes import *
from functions import *

def main():

    debugFilePath = 'D:\\4_�ҵ���Ŀ\\PythonС����\\debug dp snooplen����\\showloggingdebug'

    prefuncResult = prefunc(debugFilePath)
    num = prefuncResult['num']
    timeList = prefuncResult['timeList']
    frameList = prefuncResult['frameList']

    ###���packets���������-->###
    packetList = num *[{}]
    for i in range(num):
        f = frameList[i]
        packetList[i] = Packet(i)
        packetList[i].frame = frameList[i]
        packetList[i].timeStamp = timeList[i]
        packetList[i].dstMac = f[:4] + '.' + f[4:8]  + '.' +  f[8:12]
        packetList[i].srcMac = f[12:16] + '.' + f[16:20] + '.' + f[20:24]
        if f[24:28] in etherTypeDic.keys():
            packetList[i].etherType = etherTypeDic[f[24:28]]
        else:
            packetList[i].etherType = 'Other'
    ###<--���packets���������###


    ###��ӡPPPoE���û�������-->###
    for i in range(num):
        if packetList[i].etherType == 'PPPoE Session Stage':
            if frameList[i][40:44] == 'c023' and framesList[i][44:46] == '01':
                print 'PPPoE Username:' + getPPPoEUnPw(frameList[i])['Username']
                print 'PPPoE Password:' + getPPPoEUnPw(frameList[i])['Password']
    ###<--��ӡPPPoE���û�������###

    ###��ӡ����packet����̫����-->###
##    for i in range(num):
##        print str(i+1) + ':' + packetList[i].etherType
    ###<--��ӡ����packet����̫����###

    print 'Packet No. 1 :'
    print packetList[0]

if __name__ == '__main__':
    main()
