# -*- coding: cp936 -*-
import re

###内置对应关系表-->###
etherTypeDic = {
    '0800':'IP',
    '0806':'ARP',
    '0808':'Frame Relay ARP',
    '6559':'Raw Frame Relay',
    '8035':'RARP',
    '80F3':'AARP',
    '8137':'IPX',
    '814C':'SNMP',
    '86DD':'IPv6',
    '880B':'PPP',
    '8847':'MPLS Unicast',
    '8848':'MPLS Multicast',
    '8863':'PPPoE Discovery Stage',
    '8864':'PPPoE Session Stage',
    '88CC':'LLDP',
    '8E88':'EAPOL',
    '9100':'Vlan Tag Protocol Identifier',
    '9200':'Vlan Tag Protocol Identifier'
    }

#IPTypeDic = {
    
asciiList = ['NUL','SOH','STX','ETX','EOT','ENQ','ACK','BEL','BS','HT','LF','VT','FF','CR','SO','SI','DLE','DC1','DC2','DC3','DC4','NAK','SYN','ETB','CAN','EM','SUB','ESC','FS','GS','RS','US','SPACE','!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[','\\',']','^','_','`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','{','|','}','~','DEL']

###<--内置对应关系表###



def getPPPoEUnPw(frame):
    UnLen = int(frame[52:54],16)
    UnAscii = frame[54:(54+UnLen*2)]
    PwAscii = frame[(56+UnLen*2):]

    tmp = []
    l = len(UnAscii)
    for i in range(0,l,2):
        tmp.append(UnAscii[i:i+2])
    UnChars = []
    for i in range(l/2):
        UnChars.append(asciiList[int(tmp[i],16)])
    UnString = ''.join(UnChars)
    
    tmp = []
    l = len(PwAscii)
    for i in range(0,l,2):
        tmp.append(PwAscii[i:i+2])
    PwChars = []
    for i in range(l/2):
        PwChars.append(asciiList[int(tmp[i],16)])
    PwString = ''.join(PwChars)

    return {'Username':UnString,'Password':PwString}




###定义Packet类以及几种子类-->###
class Packet(object):
    def __init__(self,index):
        self.index = index
        self.timeStamp = None
        self.srcMac = None
        self.dstMac = None
        self.etherType  = None

    def getTimeStamp(self):
        return self.timeStamp


    
###<--定义Packet类以及几种子类###



debugFilePath = 'C:\\Users\\xwanga\\Desktop\\巴颜喀拉PPPoE获取不到地址\\PAP-debug-1.txt'

snoopLenFile = open(debugFilePath,'r',0)
snoopLenLines = snoopLenFile.readlines()

token = '------------------------------------------------\n'
l1 = len(snoopLenLines)
framesNum = snoopLenLines.count(token) / 2


timeList = []
framesList = framesNum * ['']
packetsList = framesNum * [{}]




###获取debug报文的时间戳列表-->###
for i in range(l1):
    tmp = re.findall(r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)',snoopLenLines[i])
    if len(tmp) == 1:
        timeList.append(tmp[0])
###<--获取debug报文的时间戳列表###


###获取debug报文的十六进制码列表-->###
for i in range(framesNum):
    snoopLenLines = snoopLenLines[snoopLenLines.index(token)+1:]
    x = 0
    while True:
        if snoopLenLines[x] != token:
            framesList[i] += snoopLenLines[x]
            x += 1
        else:
            snoopLenLines = snoopLenLines[snoopLenLines.index(token)+1:]
            break

for i in range(framesNum):
    framesList[i] = framesList[i].replace('\n','').replace(' ','')
###<--获取debug报文的十六进制码列表###


###判断时间戳列表和报文十六进制码列表是否长度一致-->###
if not len(timeList) == len(framesList):
    print 'Error, timestamp number not equals to frames nubmer!!!'
###<--判断时间戳列表和报文十六进制码列表是否长度一致###




for i in range(framesNum):
    f = framesList[i]
    packetsList[i] = Packet(i)
    packetsList[i].timeStamp = timeList[i]
    packetsList[i].dstMac = f[:4] + '.' + f[4:8]  + '.' +  f[8:12]
    packetsList[i].srcMac = f[12:16] + '.' + f[16:20] + '.' + f[20:24]
    if f[24:28] in etherTypeDic.keys():
        packetsList[i].etherType = etherTypeDic[f[24:28]]
    else:
        packetsList[i].etherType = 'Other'



for i in range(framesNum):
    if packetsList[i].etherType == 'PPPoE Session Stage':
        if framesList[i][40:44] == 'c023' and framesList[i][44:46] == '01':
            print 'PPPoE Username:' + getPPPoEUnPw(framesList[i])['Username']
            print 'PPPoE Password:' + getPPPoEUnPw(framesList[i])['Password']
