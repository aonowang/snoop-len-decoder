# -*- coding: cp936 -*-
###定义Packet类以及几种子类-->###
class Packet(object):
    def __init__(self,index):
        self.index = index
        self.frame = None
        self.timeStamp = None
        self.srcMac = None
        self.dstMac = None
        self.etherType  = None

    def __str__(self):
        tmp = ' '.join(self.frame[i:i+2] for i in range(0,len(self.frame),2))
        return '\n'.join(tmp[i:i+48] for i in range(0,len(tmp),48))
        
    def getTimeStamp(self):
        return self.timeStamp


    
###<--定义Packet类以及几种子类###
