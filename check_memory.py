#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#��õ�ǰ�����ڴ�Ĵ���(������λ��K)
def L_FreeMemory(nWarningSize):
	strCommandLine  = "free | grep 'Mem:' | awk '{print $2}'"
	strCurrFreeMemory = os.popen(strCommandLine).read()
	#print("[L_FreeMemory]Free memory=%d" %(int(strCurrFreeMemory)))
	if(strCurrFreeMemory < nWarningSize):
		return True
	else:
		return False
		
#���Դ���		
#if __name__ == "__main__": 
#	 if(True == L_FreeMemory(1*1024*1024)):
#		print "[L_FreeMemory]Free Memory is more"
		