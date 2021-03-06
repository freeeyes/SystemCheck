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
	if(len(list) < 6):
		strText = "链接状态不正常(" + strHostIP + ":" + strPort + ")"
		return strText		
		
	if list[5].strip() == "ESTABLISHED":
		strText = "链接从(" + list[3].strip() + ")到(" + list[4].strip() + ") 状态为[正常]" 
	else:
		strText = "[error]链接从(" + list[3].strip() + ")到(" + list[4].strip() + ") 状态为[" + list[5].strip() + "]" 
	return strText
	
def L_Telnet_Listen(strPort):
	strCommand = "netstat -an | grep LISTEN | grep " + strPort
	RetList = commands.getstatusoutput(strCommand)
	#print str(RetList[1])
	if(len(RetList) < 2):
		strText = "没有找到监听端口(" + strPort + ")"
		return strText
	list = RetList[1].split()
	#print "[L_Telnet_Listen]list=" + str(len(list))
	#print "[L_Telnet_Listen]list[5]=" + str(list[5])
	if(len(list) < 6):
		strText = "[error]监听状态不正常(" + strPort + ")"
		return strText		
	
	if list[5].strip() == "LISTEN":
		strText = "监听端口(" + strPort + ") 状态为[正常]" 
	else:
		strText = "[error]监听端口(" + strPort + ") 状态为[" + list[5].strip() + "]" 
	return strText	

'''		
#测试代码
if __name__ == "__main__":
	#print L_Telnet("124.117.209.132", "10050")
	
	print L_Telnet_Listen("8010")
'''
	