#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#获得当前空余内存的存量(参数单位是K)
def L_FreeMemory(nWarningSize):
	strCommandLine  = "free | grep 'Mem:' | awk '{print $2}'"
	strCurrFreeMemory = os.popen(strCommandLine).read()
	#print("[L_FreeMemory]Free memory=%d" %(int(strCurrFreeMemory)))
	if(strCurrFreeMemory < nWarningSize):
		return True
	else:
		return False
		
#测试代码		
#if __name__ == "__main__": 
#	 if(True == L_FreeMemory(1*1024*1024)):
#		print "[L_FreeMemory]Free Memory is more"
		