#!/usr/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import traceback
from check_process import *
from check_conf import *
from check_CPU import *
from check_memory import *
from check_disk import *
from check_logfile import *
from check_telnet import *
from Send_mail import *
from check_queue import *
from check_oracle import *

#add by freeeyes

if __name__ == "__main__": 
	try:
		nSuccess = 0
		nError   = 0
		
		objCurrDBInfo = COracleDBInfo()
		L_ReadDBConf("../conf/DB.conf", objCurrDBInfo)

		strText = ""
		# = C_Mail_Html_Begin(strText)
		#strText = C_Mail_CSS(strText)
		#strText = C_Mail_Body_Begin(strText)
		strText = C_Mail_Table_Begin(strText)
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 3, "title", "服务器自检")
		strText = C_Mail_TR_End(strText)

		objConfigSysInfo = CConfigSysInfo()
		L_ReadSysConf("../conf/sys.conf", objConfigSysInfo)
		
		#检测CPU
		blRet, nCurrCurrRote=L_CPURote(objConfigSysInfo.m_nCpu)
		if(True==blRet):
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", "CPU使用率(" + str(objConfigSysInfo.m_nCpu) +")")
			strText = C_Mail_TD(strText, 0, "content", "CPU当前使用率(" + str(nCurrCurrRote) +")")
			strText = C_Mail_TD(strText, 0, "error", "[error]过高")
			strText = C_Mail_TR_End(strText)
			nError  = nError + 1
		else:
			if(objConfigSysInfo.m_nErrSend == 0):
				strText  = C_Mail_TR_Begin(strText)
				strText  = C_Mail_TD(strText, 0, "title", "CPU使用率(" + str(objConfigSysInfo.m_nCpu) +")")
				strText  = C_Mail_TD(strText, 0, "content", "CPU当前使用率(" + str(nCurrCurrRote) +")")
				strText  = C_Mail_TD(strText, 0, "content", "正常")
				strText  = C_Mail_TR_End(strText)	
				nSuccess = nSuccess + 1
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""				
		#检测内存剩余
		blRet, strMemoryText=L_FreeMemory(objConfigSysInfo.m_nFreeMemory)
		if(True==blRet):
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", "内存使用率(" + str(objConfigSysInfo.m_nFreeMemory) +")")
			strText = C_Mail_TD(strText, 0, "error", strMemoryText)
			strText = C_Mail_TD(strText, 0, "error", "[error]过高")
			strText = C_Mail_TR_End(strText)
			nError  = nError + 1
		else:
			if(objConfigSysInfo.m_nErrSend == 0):
				strText  = C_Mail_TR_Begin(strText)
				strText  = C_Mail_TD(strText, 0, "title", "内存使用率(" + str(objConfigSysInfo.m_nFreeMemory) +")")
				strText  = C_Mail_TD(strText, 0, "content", strMemoryText)
				strText  = C_Mail_TD(strText, 0, "content", "正常")
				strText  = C_Mail_TR_End(strText)
				nSuccess = nSuccess + 1
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""				
		#检测硬盘使用率
		strDiskText, strDiskContent = L_disk(objConfigSysInfo.m_nDiskFreeAlarm)
		if(objConfigSysInfo.m_nErrSend == 0):
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", "硬盘使用率(" + str(objConfigSysInfo.m_nDiskFreeAlarm) + ")")
			if(strDiskText == ""):
				strText  = C_Mail_TD(strText, 0, "content", strDiskContent)
				strText  = C_Mail_TD(strText, 0, "content", "所有硬盘空间正常")
				nSuccess = nSuccess + 1
			else:
				strText  = C_Mail_TD(strText, 0, "content", strDiskContent)
				strText = C_Mail_TD(strText, 0, "error", strDiskText)
				nError  = nError + 1
			strText = C_Mail_TR_End(strText)
		else:
			strText = C_Mail_TR_Begin(strText)
			strText = C_Mail_TD(strText, 0, "title", "硬盘使用率(" + str(objConfigSysInfo.m_nDiskFreeAlarm) + ")")
			if(strDiskText != ""):
				strText = C_Mail_TD(strText, 0, "error", strDiskText)
				nError  = nError + 1
			strText = C_Mail_TR_End(strText)
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""
		#检测TCP链接
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 3, "title", "(" + objConfigSysInfo.m_strName + ")链接检测")
		strText = C_Mail_TR_End(strText)
		objTcpList = CTCPList()
		L_ReadTCPConf("../conf/telnet.conf", objTcpList)
		for nindex in range(0, objTcpList.GetListCount()):
			objInfo = objTcpList.GetTcpInfo(nindex)
			strTelnetText = ""
			if(objInfo.m_nType == 0):
				strTelnetText = L_Telnet(objInfo.m_strIP, objInfo.m_strPort)
			else:
				strTelnetText = L_Telnet_Listen(objInfo.m_strPort)
			objInfo = objTcpList.GetTcpInfo(nindex)
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD(strText, 0, "title", objInfo.m_strIP + ":" + objInfo.m_strPort + "(" + objInfo.m_strName + ")")
				if("error" in strTelnetText):
					strText = C_Mail_TD(strText, 0, "error", strTelnetText)
					strText = C_Mail_TD(strText, 0, "error", strTelnetText)
					nError  = nError + 1
				else:
					strText  = C_Mail_TD(strText, 0, "content", strTelnetText)
					strText  = C_Mail_TD(strText, 0, "content", "正常")
					nSuccess = nSuccess + 1
				strText = C_Mail_TR_End(strText)
			else:
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD(strText, 0, "title", objInfo.m_strIP + ":" + objInfo.m_strPort)
				if("error" in strTelnetText):
					strText = C_Mail_TD(strText, 0, "error", strTelnetText)
					nError  = nError + 1			
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""		
		#检测主要的进程
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 3, "title", "(" + objConfigSysInfo.m_strName + ")进程检测")
		strText = C_Mail_TR_End(strText)		
		objProcessList = CProcessList()
		L_ReadProcessConf("../conf/process.conf", objProcessList)
		 
		for nindex in range(0, objProcessList.GetListCount()):
			objInfo = objProcessList.GetPrecessInfo(nindex)
			if(objConfigSysInfo.m_nErrSend == 0):
				objRet,nProcessCount = L_Process(objInfo.m_strProcessName, objInfo.m_nProcessCount)
				if objRet == True:
					#print("(%d)m_strProcessName=%s OK" %(nindex, objInfo.m_strProcessName))	
					strText  = C_Mail_TR_Begin(strText)
					strText  = C_Mail_TD(strText, 0, "title", objInfo.m_strProcessName + "(" + str(objInfo.m_nProcessCount) + ")")
					strText  = C_Mail_TD(strText, 0, "content", "进程数(" + str(nProcessCount) + ")")
					strText  = C_Mail_TD(strText, 0, "content", "正常")
					strText  = C_Mail_TR_End(strText)
					nSuccess = nSuccess + 1
				else:
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD(strText, 0, "title", objInfo.m_strProcessName + "(" + str(objInfo.m_nProcessCount) + ")")
					strText = C_Mail_TD(strText, 0, "content", "进程数(" + str(nProcessCount) + ")")
					strText = C_Mail_TD(strText, 0, "error", "进程数不正常")
					strText = C_Mail_TR_End(strText)
					nError  = nError + 1
			else:
				objRet = L_Process(objInfo.m_strProcessName, objInfo.m_nProcessCount)
				if objRet == False:
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD(strText, 0, "title", objInfo.m_strProcessName + "(" + str(objInfo.m_nProcessCount) + ")")
					strText = C_Mail_TD(strText, 0, "content", "进程数(" + str(nProcessCount) + ")")
					strText = C_Mail_TD(strText, 0, "error", "进程数不正常")
					strText = C_Mail_TR_End(strText)
					nError  = nError + 1
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""					
		#检测日志文件	
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 3, "title", "(" + objConfigSysInfo.m_strName + ")日志检测")
		strText = C_Mail_TR_End(strText)		
		objLogList = CLogList()
		L_ReadLogConf("../conf/log.conf", objLogList)
		for nindex in range(0, objLogList.GetListCount()):
			objInfo = objLogList.GetLogInfo(nindex)
			print("[main]m_strLogName=%s,m_strLogKey=%s,m_nCheckLine=%d,m_nTimeInterval=%d" %(objInfo.m_strLogName, objInfo.m_strLogKey, objInfo.m_nCheckLine, objInfo.m_nTimeInterval))
			if(objInfo.m_strLogType == 1):
				objRet = L_LogFile_Daily(objInfo.m_strPath, objInfo.m_strLogName, objInfo.m_strLogKey, objInfo.m_nCheckLine, objInfo.m_nTimeInterval)
			else:
				objRet = L_LogFile_No_Daily(objInfo.m_strPath, objInfo.m_strLogName, objInfo.m_strLogKey, objInfo.m_nCheckLine, objInfo.m_nTimeInterval)
			if objRet == 0:	
				if(objConfigSysInfo.m_nErrSend == 0):
					strText  = C_Mail_TR_Begin(strText)
					strText  = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
					strText  = C_Mail_TD(strText, 0, "content", "正常")
					strText  = C_Mail_TD(strText, 0, "content", "正常")
					strText  = C_Mail_TR_End(strText)
					nSuccess = nSuccess + 1
			elif objRet == 1:
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TD(strText, 0, "error", "日志中不包含指定的关键字(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TD(strText, 0, "error", "日志中不包含指定的关键字(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TR_End(strText)
				nError  = nError + 1
			elif objRet == 2:
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TD(strText, 0, "error", "日志在指定时间内没有更新(" + str(objInfo.m_nTimeInterval) + ")")
				strText = C_Mail_TD(strText, 0, "error", "日志在指定时间内没有更新(" + str(objInfo.m_nTimeInterval) + ")")
				strText = C_Mail_TR_End(strText)
				nError  = nError + 1
			elif objRet == 3:
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD(strText, 0, "title", objInfo.m_strLogName + "(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TD(strText, 0, "error", "日志中包含指定的关键字(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TD(strText, 0, "error", "日志中包含指定的关键字(" + objInfo.m_strLogKey + ")")
				strText = C_Mail_TR_End(strText)
				nError  = nError + 1				
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""		
		#检测消息队列
		strText = C_Mail_TR_Begin(strText)
		strText = C_Mail_TD(strText, 3, "title", "(" + objConfigSysInfo.m_strName + ")消息队列")
		strText = C_Mail_TR_End(strText)
		objQueueList = CQueueList()
		L_ReadQueueConf("../conf/queue.conf", objQueueList)
		strQueueText = "" 
		for nindex in range(0, objQueueList.GetListCount()):
			objInfo = objQueueList.GetQueueInfo(nindex)
			strQueueText, nCurrQueueCount = L_LinuxQueue(objInfo.m_strQueueID, objInfo.m_nCount)
			if("error" in strQueueText):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD(strText, 0, "title", objInfo.m_strQueueID + "(" + str(objInfo.m_nCount) + ")")
				strText = C_Mail_TD(strText, 0, "content", objInfo.m_strQueueID + "当前数量(" + str(nCurrQueueCount) + ")")
				strText = C_Mail_TD(strText, 0, "error", strQueueText)
				strText = C_Mail_TR_End(strText)
				nError  = nError + 1			
			else:
				if(objConfigSysInfo.m_nErrSend == 0):
					strText  = C_Mail_TR_Begin(strText)
					strText  = C_Mail_TD(strText, 0, "title", objInfo.m_strQueueID + "(" + str(objInfo.m_nCount) + ")")
					strText  = C_Mail_TD(strText, 0, "content", objInfo.m_strQueueID + "当前数量(" + str(nCurrQueueCount) + ")")
					strText  = C_Mail_TD(strText, 0, "content", "正常")
					strText  = C_Mail_TR_End(strText)
					nSuccess = nSuccess + 1	
		strText = C_Mail_Table_End(strText)
		L_Oracle_Save_Info(objCurrDBInfo, objConfigSysInfo.m_strName, strText);	
		strText = ""	

		'''
		if(objConfigSysInfo.m_nErrSend == 1 and nError > 0):
			objMailInfo = CMailInfo()
			L_ReadMailConf("../conf/mail.conf", objMailInfo)
			strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "自检邮件"
			L_SendMail(objMailInfo, strMailTitle, strText)
		else:
			objMailInfo = CMailInfo()
			L_ReadMailConf("../conf/mail.conf", objMailInfo)
			strMailTitle = "(" + objConfigSysInfo.m_strName + ")" + "自检邮件"
			L_SendMail(objMailInfo, strMailTitle, strText)
		'''
	except Exception,e:
		#print "[main error]",Exception,":",e
		print traceback.format_exc()