# -*- coding: cp936 -*-
###PPPoE报文的用户名密码提取函数-->###
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
###<--PPPoE报文的用户名密码提取函数###
