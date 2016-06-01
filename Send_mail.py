#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 
import smtplib
import base64
from email.mime.text import MIMEText 
from check_conf import * 

#发送邮件
def L_SendMail_SSL(objMailInfo, strTitle, strText):
	#mail_to   = "shiqianga@si-tech.com.cn" 
	#mail_host = "smtp.qq.com"  #设置服务器
	#mail_user = "41198969"    #用户名
	#mail_pass = "dwghwgzkdrwdbgjg"   #口令 

	#msg = MIMEText(strText, _subtype='plain', _charset='gb2312')  
	msg = MIMEText(strText, _subtype='html', _charset='gb2312')  
	msg['Subject'] = strTitle 
	msg['From']    = objMailInfo.m_strMailFrom
	msg['To']      = objMailInfo.m_strMailTo
	
	try:  
		server = smtplib.SMTP(objMailInfo.m_strMailHost, objMailInfo.m_nMailPort)  

		#server.set_debuglevel(1)
		server.ehlo()
		server.starttls()
		server.login(objMailInfo.m_strUser, objMailInfo.m_strPass)
		server.sendmail(objMailInfo.m_strMailFrom, objMailInfo.m_strMailTo, msg.as_string())
		
		server.close()  
		return True  
	except Exception, e:  
		print str(e)  
		return False
		
#发送邮件
def L_SendMail(objMailInfo, strTitle, strText):
	#msg = MIMEText(strText, _subtype='plain', _charset='gb2312')  
	msg = MIMEText(strText, _subtype='html', _charset='gb2312')  
	msg['Subject'] = strTitle 
	msg['From']    = objMailInfo.m_strMailFrom
	msg['To']      = objMailInfo.m_strMailTo
	
	try:  
		print objMailInfo.m_strMailHost + ":" + str(objMailInfo.m_nMailPort)
		server = smtplib.SMTP(objMailInfo.m_strMailHost)  

		server.set_debuglevel(1)
		server.ehlo("chandao@teamshub.com")
		#server.starttls()
		print objMailInfo.m_strUser + ":" + objMailInfo.m_strPass
		#server.login(objMailInfo.m_strUser, objMailInfo.m_strPass)
		server.esmtp_features["auth"] = "LOGIN"
		server.login("chandao@teamshub.com", "404104")
		print objMailInfo.m_strMailFrom + ":" + objMailInfo.m_strMailTo
		server.sendmail(objMailInfo.m_strMailFrom, objMailInfo.m_strMailTo, msg.as_string())
		
		server.close()  
		return True  
	except Exception, e:  
		print str(e)  
		return False		

#邮件样式表
def C_Mail_CSS(strCSS):
	strCSS = strCSS + "<head><style type=‘text/css’> \
			.title { color: red; font-size: 15px; background-color:#D6D6D6; }\
			.content { color: blue; font-size: 15px; background-color:#C7EDCC; }\
			</style>\
			</head>"
	return strCSS
	
#邮件的头
def C_Mail_Html_Begin(strText):
	strText = "<ifream id='freeeyes' width=100% height=100%>"
	strText = strText + "<html xmlns='http://www.w3.org/1999/xhtml'>"
	return strText
	
#邮件的尾巴
def C_Mail_Html_End(strText):
	strText = strText + "</html></ifream>"
	return strText
	
#邮件的体头	
def C_Mail_Body_Begin(strText):
	strText = strText + "<body style='margin: 0; padding: 0;'>"
	return strText

#邮件的体尾	
def C_Mail_Body_End(strText):
	strText = strText + "</body>"
	return strText
	
#邮件的表头
def C_Mail_Table_Begin(strText):
	strText = strText + "<table border='1' cellpadding='0' cellspacing='0' width='100%'>"
	return strText

#邮件的表尾
def C_Mail_Table_End(strText):
	strText = strText + "</table>"
	return strText
	
#邮件的tr头
def C_Mail_TR_Begin(strText):
	strText = strText + "<tr>"
	return strText
	
#邮件的tr尾	
def C_Mail_TR_End(strText):
	strText = strText + "</tr>"
	return strText	

#邮件的td
def C_Mail_TD(strText, nColspan, strClass, strContent):
	if(nColspan > 0):
		strText = strText + "<td colspan='" + str(nColspan) + "' class='" + strClass + "'>" + strContent + "</td>"
	else:
		strText = strText + "<td class='" + strClass + "'>" + strContent + "</td>"
	return strText
	
#邮件的td
def C_Mail_TD_WIDTH(strText, nColspan, strClass, strContent, nWidth):
	if(nColspan > 0):
		strText = strText + "<td width='" + str(nWidth) + "%' colspan='" + str(nColspan) + "' class='" + strClass + "'>" + strContent + "</td>"
	else:
		strText = strText + "<td width='" + str(nWidth) + "%' class='" + strClass + "'>" + strContent + "</td>"
	return strText	
				
#测试代码		
if __name__ == "__main__":
	objMailInfo = CMailInfo()
	L_ReadMailConf("./mail.conf", objMailInfo)
	
	L_SendMail(objMailInfo, "自测邮件", "Test")		