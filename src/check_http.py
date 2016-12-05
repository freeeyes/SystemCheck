#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import time
import json
import urllib
import urllib2 
from Send_mail import *

reload(sys)
sys.setdefaultencoding('utf-8')

#Json文件信息配置
class CConfigHTTP:
	def __init__(self):
		self.m_strName       = ""
		self.m_strHttpURL    = ""
		self.m_nHttpType     = 1   #1 get 2 post
		self.m_strData       = ""
		self.m_strReturn     = ""

#读取配置文件
def L_Http_Info(strCfgFile, objHttpList):
	try:
		f = open(strCfgFile)
		line = f.readline()
		#print line 
		while line:
			strJson = line
			#print strJson 
			d = json.loads(strJson, encoding="GB2312")

			#根据配置文件解析数据
			bjInfo = CConfigHTTP()
			
			bjInfo.m_strName    = d["NAME"]
			bjInfo.m_strHttpURL = d['URL']
			bjInfo.m_nHttpType  = int(d['TYPE'])
			bjInfo.m_strData    = d['SendData']
			bjInfo.m_strReturn  = d['RecvData']
			
			#print("m_strHttpURL=%s" %(bjInfo.m_strHttpURL))
			#print("m_nHttpType=%d" %(bjInfo.m_nHttpType))
			#print("m_strData=%s" %(bjInfo.m_strData))
			#print("m_strReturn=%s" %(bjInfo.m_strReturn))
			
			objHttpList.append(bjInfo)
		
			line = f.readline()  
		f.close()
	except Exception,e:
		s=sys.exc_info()
		print("<p>[error]<%d>(%s)</p>" %(s[2].tb_lineno, e))	
		
#发送测试数据
def L_Http_Test(strName, strURL, nType, strData, strRecv):
	try:	
		if(nType == 2):
			#POST
			#print("[L_HttpTest]URL=%s" %(objHttpList[nindex].m_strHttpURL))
			f = urllib2.urlopen(strURL, strData)
			content = f.read()
			#print("[L_HttpTest]content=%s" %(content))
			#print("[L_HttpTest]strRecv=%s" %(strRecv))
			if(strRecv in content):
				return True,""
			else:
				strError="<" + strURL + "><" + content + ">"
				return False,strError	
		else:
			#GET
			f = urllib2.urlopen(strURL)
			content = f.read()
			#print("[L_HttpTest]content=%s" %(content))
			if(strRecv in content):
				return True,""
			else:
				strError="<" + strName + "><" + content + ">"
				return False,strError					
	except Exception,e:
		#s=sys.exc_info()
		#print("<p>[error]<%d>(%s)</p>" %(s[2].tb_lineno, e))
		strError="<" + strName + ">[error]<" + str(e) + ">"
		return False,strError		
			
		
#按照数组组合发送数据
def L_Http_List(objHttpList, objMailText):
	for nindex in range(0, len(objHttpList)):
		blret,strDtata = L_Http_Test(objHttpList[nindex].m_strName,
																 objHttpList[nindex].m_strHttpURL, 
																 objHttpList[nindex].m_nHttpType, 
																 objHttpList[nindex].m_strData, 
																 objHttpList[nindex].m_strReturn)
		if(blret == False):
			print("<p>[%s]%s</p>" %(time.strftime('%Y-%m-%d %X', time.localtime()), strDtata))
			objMailText.append(strDtata)
		else:
			print("[%s]<%s>OK" %(time.strftime('%Y-%m-%d %X', time.localtime()), objHttpList[nindex].m_strName))
			
	if(len(objMailText) > 0):
		strText = ""
		for i in range(0, len(objMailText)):
			strText += objMailText[i]
		
		#发送告警邮件
		L_ReadMailConf("../conf/mail.conf", objMailInfo)
		strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "自检邮件"
		L_SendMail(objMailInfo, strMailTitle, strText)	
		
#测试代码	
if __name__ == "__main__":
	objHttpList = []
	objMailText = []
	
	L_Http_Info("../conf/http.conf", objHttpList)
	
	L_Http_List(objHttpList, objMailText)
 
