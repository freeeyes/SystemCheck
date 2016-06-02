#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#检查进程个数，是否一致
def L_Process(strPrecessName, nCount):
	strCommandLine = "ps -ef | grep -w " + strPrecessName + " | grep -v grep |awk '{print $2}' | wc -l"
	#print("[L_Process]Command=%s" % strCommandLine)
	strCurrCount   = os.popen(strCommandLine).read()
	#print("[L_Process]strCurrCount=%s" % strCurrCount)
	nCurrCount     = int(strCurrCount)
	
	if(nCurrCount <> nCount):
		print("[L_Process]%s CurrCount=%d,count=%d" %(strPrecessName, nCurrCount, nCount))
		return False
	else:
		return True;
		
#if __name__ == "__main__": 
#	 L_Process("lkyw_service", 2)