#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
from check_process import *
from check_conf import *
from check_CPU import *
from check_memory import *
from check_disk import *
from check_logfile import *
from Send_mail import *

#add by freeeyes

if __name__ == "__main__": 
	strText = ""
	strText = C_Mail_Html_Begin(strText)
	strText = C_Mail_CSS(strText)
	strText = C_Mail_Body_Begin(strText)
	strText = C_Mail_Table_Begin(strText)
	strText = C_Mail_TR_Begin(strText)
	strText = C_Mail_TD(strText, 2, "title", "(�½��ӿڻ�1)�������Լ�")
	strText = C_Mail_TR_End(strText)

	objConfigSysInfo = CConfigSysInfo()
	L_ReadSysConf("./sys.conf", objConfigSysInfo)
	
	#���CPU
	if(True==L_CPURote(objConfigSysInfo.m_nCpu)):
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 0, "title", "CPUʹ����(" + str(objConfigSysInfo.m_nCpu) +")")
		strText = C_Mail_TD(strText, 0, "content", "����")
		strText = C_Mail_TR_End(strText)	
	else:
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 0, "title", "CPUʹ����(" + str(objConfigSysInfo.m_nCpu) +")")
		strText = C_Mail_TD(strText, 0, "content", "����")
		strText = C_Mail_TR_End(strText)	
	#����ڴ�ʣ��
	if(True==L_FreeMemory(objConfigSysInfo.m_nFreeMemory)):
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 0, "title", "�ڴ�ʹ����(" + str(objConfigSysInfo.m_nFreeMemory) +")")
		strText = C_Mail_TD(strText, 0, "content", "����")
		strText = C_Mail_TR_End(strText)	
	else:
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 0, "title", "�ڴ�ʹ����(" + str(objConfigSysInfo.m_nFreeMemory) +")")
		strText = C_Mail_TD(strText, 0, "content", "����")
		strText = C_Mail_TR_End(strText)	
	#�����Ҫ�Ľ���
	strText = C_Mail_TD(strText, 2, "title", "(�½��ӿڻ�1)���̼��")
	strText = C_Mail_TR_End(strText)		
	objProcessList = CProcessList()
	L_ReadProcessConf("./process.conf", objProcessList)
	 
	for nindex in range(0, objProcessList.GetListCount()):
		objInfo = objProcessList.GetPrecessInfo(nindex)
		objRet = L_Process(objInfo.m_strProcessName, objInfo.m_nProcessCount)
		if objRet == True:
			#print("(%d)m_strProcessName=%s OK" %(nindex, objInfo.m_strProcessName))	
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strProcessName + "(" + str(objInfo.m_nProcessCount) + ")")
			strText = C_Mail_TD(strText, 0, "content", "����")
			strText = C_Mail_TR_End(strText)
		else:
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strProcessName + "(" + str(objInfo.m_nProcessCount) + ")")
			strText = C_Mail_TD(strText, 0, "content", "������������")
			strText = C_Mail_TR_End(strText)
	#�����־�ļ�	
	strText = C_Mail_TD(strText, 2, "title", "(�½��ӿڻ�1)��־���")
	strText = C_Mail_TR_End(strText)		
	objLogList = CLogList()
	L_ReadLogConf("./log.conf", objLogList)

	for nindex in range(0, objLogList.GetListCount()):
		objInfo = objLogList.GetPrecessInfo(nindex)
		print("[main]m_strLogName=%s,m_strLogKey=%s,m_nCheckLine=%d,m_nTimeInterval=%d" %(objInfo.m_strLogName, objInfo.m_strLogKey, objInfo.m_nCheckLine, objInfo.m_nTimeInterval))
		objRet = L_LogFile_Daily(objInfo.m_strPath, objInfo.m_strLogName, objInfo.m_strLogKey, objInfo.m_nCheckLine, objInfo.m_nTimeInterval)
		if objRet == 0:	
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
			strText = C_Mail_TD(strText, 0, "content", "����")
			strText = C_Mail_TR_End(strText)
		elif objRet == 1:
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
			strText = C_Mail_TD(strText, 0, "content", "��־�в�����ָ���Ĺؼ���(" + objInfo.m_strLogKey + ")")
			strText = C_Mail_TR_End(strText)
		else:
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
			strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
			strText = C_Mail_TD(strText, 0, "content", "��־��ָ��ʱ����û�и���(" + str(objInfo.m_nTimeInterval) + ")")
			strText = C_Mail_TR_End(strText)			
	
	strText = C_Mail_Table_End(strText)
	strText = C_Mail_Body_End(strText)
	strText = C_Mail_Html_End(strText)
	
	L_SendMail("�Բ��ʼ�", strText)