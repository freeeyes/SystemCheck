#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#��õ�ǰCPU��ʹ�ðٷ���
def L_CPURote(nWarningRote):
	strCommandLine  = "vmstat 1 2 | tail -1 | awk '{print $15}'"
	strCurrIdelRote = os.popen(strCommandLine).read()
	#print("[L_CPURote]idel=%d" %(int(strCurrIdelRote)))
	nCurrUsedRote = 100 - int(strCurrIdelRote)
	if(nCurrUsedRote >= nWarningRote):
		return True
	else:
		return False

#���Դ���		
#if __name__ == "__main__": 
#	 if(True == L_CPURote(80)):
#		print "[L_CPURote]CPU is more"
