#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 
import smtplib
import base64
from email.mime.text import MIMEText  

#�����ʼ�
def L_SendMail(strTitle, strText):
	mail_to   = "shiqianga@si-tech.com.cn" 
	mail_host = "smtp.qq.com"  #���÷�����
	mail_user = "41198969"    #�û���
	mail_pass = "#######"   #���� 

	#msg = MIMEText(strText, _subtype='plain', _charset='gb2312')  
	msg = MIMEText(strText, _subtype='html', _charset='gb2312')  
	msg['Subject'] = strTitle 
	msg['From']    = "41198969@qq.com"
	msg['To']      = mail_to
	
	try:  
		server = smtplib.SMTP(mail_host, 25)  

		#server.set_debuglevel(1)
		server.ehlo()
		server.starttls()
		server.login(mail_user, mail_pass)
		server.sendmail("41198969@qq.com", mail_to, msg.as_string())
		
		server.close()  
		return True  
	except Exception, e:  
		print str(e)  
		return False

#�ʼ���ʽ��
def C_Mail_CSS(strCSS):
	strCSS = strCSS + "<head><style type=��text/css��> \
			.title { color: red; font-size: 15px; background-color:#D6D6D6; }\
			.content { color: blue; font-size: 15px; background-color:#C7EDCC; }\
			</style>\
			</head>"
	return strCSS
	
#�ʼ���ͷ
def C_Mail_Html_Begin(strText):
	strText = "<ifream id='freeeyes' width=100% height=100%>"
	strText = strText + "<html xmlns='http://www.w3.org/1999/xhtml'>"
	return strText
	
#�ʼ���β��
def C_Mail_Html_End(strText):
	strText = strText + "</html></ifream>"
	return strText
	
#�ʼ�����ͷ	
def C_Mail_Body_Begin(strText):
	strText = strText + "<body style='margin: 0; padding: 0;'>"
	return strText

#�ʼ�����β	
def C_Mail_Body_End(strText):
	strText = strText + "</body>"
	return strText
	
#�ʼ��ı�ͷ
def C_Mail_Table_Begin(strText):
	strText = strText + "<table border='1' cellpadding='0' cellspacing='0' width='100%'>"
	return strText

#�ʼ��ı�β
def C_Mail_Table_End(strText):
	strText = strText + "</table>"
	return strText
	
#�ʼ���trͷ
def C_Mail_TR_Begin(strText):
	strText = strText + "<tr>"
	return strText
	
#�ʼ���trβ	
def C_Mail_TR_End(strText):
	strText = strText + "</tr>"
	return strText	

#�ʼ���td
def C_Mail_TD(strText, nColspan, strClass, strContent):
	if(nColspan > 0):
		strText = strText + "<td colspan='" + str(nColspan) + "' class='" + strClass + "'>" + strContent + "</td>"
	else:
		strText = strText + "<td class='" + strClass + "'>" + strContent + "</td>"
	return strText
		
'''		
#���Դ���		
if __name__ == "__main__": 
	#ƴ�Ӳ��Ա��
	strText = ""
	strText = C_Mail_Html_Begin(strText)
	strText = C_Mail_CSS(strText)
	strText = C_Mail_Body_Begin(strText)
	strText = C_Mail_Table_Begin(strText)
	strText = C_Mail_TR_Begin(strText)
	strText = C_Mail_TD(strText, 2, "title", "���Ա���")
	strText = C_Mail_TR_End(strText)
	strText = C_Mail_TR_Begin(strText)
	strText = C_Mail_TD(strText, 0, "content", "��������TSS1")
	strText = C_Mail_TD(strText, 0, "content", "��������TSS2")
	strText = C_Mail_TR_End(strText)	
	strText = C_Mail_Table_End(strText)
	strText = C_Mail_Body_End(strText)
	strText = C_Mail_Html_End(strText)
	
	print("[strText]%s"%(strText))
	
	L_SendMail("�Բ��ʼ�", strText)		
'''