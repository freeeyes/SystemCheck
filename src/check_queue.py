#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#�����Ϣ�����Ƿ�����
def L_LinuxQueue(strQueueID, nCount):
	strCommandLine  = "ipcs -qa | grep " + strQueueID
	strCurrQueue    = os.popen(strCommandLine).read()
	strCurrText    = strCurrQueue.split()
	if(len(strCurrText) == 6):
		nCurrCount = int(strCurrText[5])
		if(nCurrCount >= nCount):
			return "(" + strQueueID + ")[error]���������ݻ�ѹ",nCurrCount
		else:
			return "(" + strQueueID + ")��������",nCurrCount
	else:
		return "(" + strQueueID + ")[error]û���ҵ�������Ϣ",nCurrCount
		
#���Դ���		
#if __name__ == "__main__": 
#	print L_LinuxQueue("4e36", 500)	