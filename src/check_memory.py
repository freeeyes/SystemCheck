#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#获得当前空余内存的存量(参数单位是K)
def L_FreeMemory(nWarningSize):
	strText = ""
	strCommandLine  = "free | grep 'Mem:'"
	strCurrFreeMemory = os.popen(strCommandLine).read()
	#print("[L_FreeMemory]Free memory=%d" %(int(strCurrFreeMemory)))
	strMenList = strCurrFreeMemory.split()
	fMemoryUser = float(float(strMenList[2]) - float(strMenList[5]) - float(strMenList[6])/float(strMenList[1])) * float(100.0)
	strText = "所有内存: " + strMenList[1]  
		+ ",使用内存: " + str(int(float(float(strMenList[2]) - float(strMenList[5]) - float(strMenList[6]))) 
		+ ",自由内存: " + str(int(float(strMenList[1]) - float(float(strMenList[2]) - float(strMenList[5]) - float(strMenList[6]))
		+ ",使用率： " + str(fMemoryUser) +"%"
	if(int(float(strMenList[1]) - float(float(strMenList[2]) - float(strMenList[5]) - float(strMenList[6]) < nWarningSize):
		return True,strText
	else:
		return False,strText
		
#测试代码		
#if __name__ == "__main__": 
#	 if(True == L_FreeMemory(1*1024*1024)):
#		print "[L_FreeMemory]Free Memory is more"
		