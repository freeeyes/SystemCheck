#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#检测消息队列是否阻塞
def L_LinuxQueue(strQueueID, nCount):
	strCommandLine  = "ipcs -qa | grep " + strQueueID
	strCurrQueue    = os.popen(strCommandLine).read()
	strCurrText    = strCurrQueue.split()
	if(len(strCurrText) == 6):
		nCurrCount = int(strCurrText[5])
		if(nCurrCount >= nCount):
			return "(" + strQueueID + ")[error]队列有数据积压",nCurrCount
		else:
			return "(" + strQueueID + ")队列正常",nCurrCount
	else:
		return "(" + strQueueID + ")[error]没有找到队列信息",nCurrCount
		
#测试代码		
#if __name__ == "__main__": 
#	print L_LinuxQueue("4e36", 500)	