#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#查看某个链接状态
def L_Telnet(strHostIP, strPort):
	strCommand = "netstat -an | grep " + strHostIP +":" + strPort
	RetList = commands.getstatusoutput(strCommand)
	#print str(RetList[1])
	if(len(RetList) < 2):
		strText = "没有找到链接(" + strHostIP + ":" + strPort + ")"
		return strText
	list = RetList[1].split()
	#print "]L_Telnet]list=" + str(len(list))
	if(len(list) != 6):
		strText = "链接状态不正常(" + strHostIP + ":" + strPort + ")"
		return strText		
	strText = "链接从(" + list[3].strip() + ")到(" + list[4].strip() + ") 状态为[" + list[5].strip() + "]" 
	return strText
	
'''	
#测试代码
if __name__ == "__main__":
	print L_Telnet("124.117.209.132", "10050")
'''	