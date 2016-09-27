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

		#输出统计结果
		#web机1
		strDBHtml = ""
		strText = strText + "<b>" + "新疆web机45" + "</b>"
		strDBHtml = L_Oracle_Load_Info(objCurrDBInfo, "新疆web机45")
		print strDBHtml
		strText = strText + strDBHtml
	
		#web机2
		strDBHtml = ""
		strText = strText + "<b>" + "新疆web机46" + "</b>"
		strDBHtml = L_Oracle_Load_Info(objCurrDBInfo, "新疆web机46")
		print strDBHtml
		strText = strText + strDBHtml
	
		#业务机
		strDBHtml = ""
		strText = strText + "<b>" + objConfigSysInfo.m_strName + "</b>"
		strDBHtml = L_Oracle_Load_Info(objCurrDBInfo, objConfigSysInfo.m_strName)
		strText = strText + strDBHtml

		strText = C_Mail_Body_End(strText)
		
		if(objConfigSysInfo.m_nErrSend == 1 and nError > 0):
			objMailInfo = CMailInfo()
			L_ReadMailConf("../conf/mail.conf", objMailInfo)
			strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "自检邮件"
			#objMailInfo.m_strMailTo = "shiqianga@si-tech.com.cn"
			L_SendMail(objMailInfo, strMailTitle, strText)
		else:
			objMailInfo = CMailInfo()
			L_ReadMailConf("../conf/mail.conf", objMailInfo)
			strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "自检邮件"
			#objMailInfo.m_strMailTo = "shiqianga@si-tech.com.cn"
			L_SendMail(objMailInfo, strMailTitle, strText)	
	except Exception,e:
		#print "[main error]",Exception,":",e
		print traceback.format_exc()
