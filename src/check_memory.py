#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#��õ�ǰ�����ڴ�Ĵ���(������λ��K)
def L_FreeMemory(nWarningSize):
	strText = ""
	strCommandLine  = "free | grep 'Mem:'"
	strCurrFreeMemory = os.popen(strCommandLine).read()
	#print("[L_FreeMemory]Free memory=%d" %(int(strCurrFreeMemory)))
	strMenList = strCurrFreeMemory.split()
	fMemoryUser = float(float(strMenList[2])/float(strMenList[1])) * float(100.0)
	strText = "�����ڴ�: " + strMenList[1]  + ",ʹ���ڴ�: " + strMenList[2] + ",�����ڴ�: " + strMenList[3] + ",ʹ���ʣ� " + str(fMemoryUser) +"%"
	if(int(strMenList[3]) < nWarningSize):
		return True,strText
	else:
		return False,strText
		
#���Դ���		
#if __name__ == "__main__": 
#	 if(True == L_FreeMemory(1*1024*1024)):
#		print "[L_FreeMemory]Free Memory is more"
		