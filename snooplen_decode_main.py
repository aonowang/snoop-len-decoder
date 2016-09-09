# -*- coding: cp936 -*-
import re

from tables import *
from prefunc import *
from classes import *
from functions import *

def main():

    debugFilePath = 'D:\\4_我的项目\\Python小工具\\debug dp snooplen解码\\showloggingdebug'

    prefuncResult = prefunc(debugFilePath)
    num = prefuncResult['num']
    timeList = prefuncResult['timeList']
    frameList = prefuncResult['frameList']

    ###填充packets对象的属性-->###
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
    ###<--填充packets对象的属性###


    ###打印PPPoE的用户名密码-->###
    for i in range(num):
        if packetList[i].etherType == 'PPPoE Session Stage':
            if frameList[i][40:44] == 'c023' and framesList[i][44:46] == '01':
                print 'PPPoE Username:' + getPPPoEUnPw(frameList[i])['Username']
                print 'PPPoE Password:' + getPPPoEUnPw(frameList[i])['Password']
    ###<--打印PPPoE的用户名密码###

    ###打印所有packet的以太类型-->###
##    for i in range(num):
##        print str(i+1) + ':' + packetList[i].etherType
    ###<--打印所有packet的以太类型###

    print 'Packet No. 1 :'
    print packetList[0]

if __name__ == '__main__':
    main()
