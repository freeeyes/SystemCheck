#!/usr/env python
# -*- coding: utf-8 -*- 
from check_oracle import *
from Send_mail import *

#add by freeeyes

if __name__ == "__main__": 
	try:
		nSuccess = 0
		nError   = 0
		
		objCurrDBInfo = COracleDBInfo()
		L_ReadDBConf("../conf/DB.conf", objCurrDBInfo)
		
		objConfigSysInfo = CConfigSysInfo()
		L_ReadSysConf("../conf/sys.conf", objConfigSysInfo)

		strText = ""
		strText = C_Mail_Html_Begin(strText)
		strText = C_Mail_CSS(strText)
		strText = C_Mail_Body_Begin(strText)

		#���ͳ�ƽ��
		#web��1
		strDBHtml = ""
		strText = strText + "<b>" + "�½�web��45" + "</b>"
		strDBHtml = L_Oracle_Load_Info(objCurrDBInfo, "�½�web��45")
		print strDBHtml
		strText = strText + strDBHtml
	
		#web��2
		strDBHtml = ""
		strText = strText + "<b>" + "�½�web��46" + "</b>"
		strDBHtml = L_Oracle_Load_Info(objCurrDBInfo, "�½�web��46")
		print strDBHtml
		strText = strText + strDBHtml
	
		#ҵ���
		strDBHtml = ""
		strText = strText + "<b>" + objConfigSysInfo.m_strName + "</b>"
		strDBHtml = L_Oracle_Load_Info(objCurrDBInfo, objConfigSysInfo.m_strName)
		strText = strText + strDBHtml

		strText = C_Mail_Body_End(strText)
		
		if(objConfigSysInfo.m_nErrSend == 1 and nError > 0):
			objMailInfo = CMailInfo()
			L_ReadMailConf("../conf/mail.conf", objMailInfo)
			strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "�Լ��ʼ�"
			#objMailInfo.m_strMailTo = "shiqianga@si-tech.com.cn"
			L_SendMail(objMailInfo, strMailTitle, strText)
		else:
			objMailInfo = CMailInfo()
			L_ReadMailConf("../conf/mail.conf", objMailInfo)
			strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "�Լ��ʼ�"
			#objMailInfo.m_strMailTo = "shiqianga@si-tech.com.cn"
			L_SendMail(objMailInfo, strMailTitle, strText)	
	except Exception,e:
		#print "[main error]",Exception,":",e
		print traceback.format_exc()
