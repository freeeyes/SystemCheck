#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#�鿴ĳ������״̬
def L_Telnet(strHostIP, strPort):
	strCommand = "netstat -an | grep " + strHostIP +":" + strPort
	RetList = commands.getstatusoutput(strCommand)
	#print str(RetList[1])
	if(len(RetList) < 2):
		strText = "û���ҵ�����(" + strHostIP + ":" + strPort + ")"
		return strText
	list = RetList[1].split()
	#print "]L_Telnet]list=" + str(len(list))
	if(len(list) != 6):
		strText = "����״̬������(" + strHostIP + ":" + strPort + ")"
		return strText		
	strText = "���Ӵ�(" + list[3].strip() + ")��(" + list[4].strip() + ") ״̬Ϊ[" + list[5].strip() + "]" 
	return strText
	
'''	
#���Դ���
if __name__ == "__main__":
	print L_Telnet("124.117.209.132", "10050")
'''	