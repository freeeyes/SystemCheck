#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#获得当前CPU的使用百分率
def L_CPURote(nWarningRote):
	strCommandLine  = "vmstat 1 2 | tail -1 | awk '{print $15}'"
	strCurrIdelRote = os.popen(strCommandLine).read()
	#print("[L_CPURote]idel=%d" %(int(strCurrIdelRote)))
	nCurrUsedRote = 100 - int(strCurrIdelRote)
	if(nCurrUsedRote >= nWarningRote):
		return True,nCurrUsedRote
	else:
		return False,nCurrUsedRote
		
def L_CPURote_Ex(nWarningRote):
	#得到当前有多少个CPU
	strCommandLine  = "cat /proc/stat | grep cpu[0-9] -c"
	strCurrCpuCount = os.popen(strCommandLine).read()
	print("[L_CPURote_Ex]CPU Count=%d" %(int(strCurrCpuCount)))
	
	for i in range(0, int(strCurrCpuCount)):
		strCommandLine  = "cat /proc/stat | grep -w \"cpu" + str(i) + "\" | awk '{print $2\" \"$3\" \"$4\" \"$5\" \"$6\" \"$7\" \"$8}'"
		#print strCommandLine
		strText = os.popen(strCommandLine).read()
		#print("[L_CPURote_Ex]CPU%d=%s" %(i, strText))
		strParamList = strText.split()
		nIdel  = int(strParamList[3])
		nTitle = int(strParamList[0]) + int(strParamList[1]) + int(strParamList[2]) + int(strParamList[3]) + int(strParamList[4]) + int(strParamList[5]) + int(strParamList[6])
		nRote = float(100) - float(nIdel)/float(nTitle) * float(100)
		print("[L_CPURote_Ex]CPU%d=%f" %(i, nRote))
		

#测试代码		
#if __name__ == "__main__": 
#	 if(True == L_CPURote(80)):
#		print "[L_CPURote]CPU is more"
	#L_CPURote_Ex(10)
