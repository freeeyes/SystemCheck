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
from check_oracle import *
from check_telnet import *
from Send_mail import *
from check_queue import *

#add by freeeyes

if __name__ == "__main__": 
	try:
		nSuccess = 0
		nError   = 0

		strText = ""
		strText = C_Mail_Html_Begin(strText)
		strText = C_Mail_CSS(strText)
		strText = C_Mail_Body_Begin(strText)
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
		#检测TCP链接
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
		
		#检测主要的进程
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
					
		#检测日志文件	
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
		
		#检测消息队列
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
		
		#检测数据库
		if(objConfigSysInfo.m_nCheckDB == 1):
			strText = C_Mail_TD(strText, 3, "title", "(" + objConfigSysInfo.m_strName + ")数据库检测")
			strText = C_Mail_TR_End(strText)
			objOracleDBInfo = COracleDBInfo()
			L_ReadDBConf("../conf/DB.conf", objOracleDBInfo)
			
			strDBText = L_Oracle_Test_User(objOracleDBInfo)
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD_WIDTH(strText, 0, "title", "账号检测", 20)
				if("error" in strDBText):
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
				else:
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBText, 40)
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", "正常", 40)
					nSuccess = nSuccess + 1
				strText = C_Mail_TR_End(strText)
			else:
				if("error" in strDBText):
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD_WIDTH(strText, 0, "title", "账号检测", 20)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					nError  = nError + 1
					strText = C_Mail_TR_End(strText)		
					
			strDBText = L_Oracle_Online_Info(objOracleDBInfo, objConfigSysInfo.m_nOnlineRote)
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD_WIDTH(strText, 0, "title", "车辆在线率", 20)
				#print "在线率:" + strDBText
				if("error" in strDBText):
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
				else:
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBText, 40)
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", "正常", 40)
					nSuccess = nSuccess + 1
				strText = C_Mail_TR_End(strText)
			else:
				if("error" in strDBText):
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD_WIDTH(strText, 0, "title", "车辆在线率", 20)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
					strText = C_Mail_TR_End(strText)		
			
			for iDeadCount in range(0,10):
				strDBText = L_Oracle_DeadLock_Info(objOracleDBInfo)
				if(strDBText != "没有死锁"):
					time.sleep(5)
				else:
					break
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD_WIDTH(strText, 0, "title", "数据库死锁", 20)
				if(strDBText == "没有死锁"):
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBText, 40)
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", "正常", 40)
					nSuccess = nSuccess + 1
				else:
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
				strText = C_Mail_TR_End(strText)
			else:
				if(strDBText != "没有死锁"):
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD_WIDTH(strText, 0, "title", "数据库死锁", 20)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
					strText = C_Mail_TR_End(strText)		
			strDBTextList, strDBContentList = L_Oracle_TableUsed_Info(objOracleDBInfo, objConfigSysInfo.m_nDBDiskRote)
			strDBText    = ""
			strDBContent = ""
			for strTemp in strDBTextList:
				strDBText    = strDBText + "<p>" + strTemp + "</p>"			
			for strTemp1 in strDBContentList:	
				strDBContent = strDBContent + "<p>" + strTemp1 + "</p>"
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD_WIDTH(strText, 0, "title", "数据库空间(" + str(objConfigSysInfo.m_nDBDiskRote) + ")", 20)
				if("error" in strDBText):
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBContent, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					nError  = nError + 1
				else:
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBContent, 40)
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBText, 40)
					nSuccess = nSuccess + 1
				strText = C_Mail_TR_End(strText)
			else:
				if("error" in strDBText):
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD_WIDTH(strText, 0, "title", "数据库空间(" + str(objConfigSysInfo.m_nDBDiskRote) + ")", 20)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBContent, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					nError  = nError + 1
					strText = C_Mail_TR_End(strText)		
			strDBTextList = L_Oracle_User_Info(objOracleDBInfo)
			strDBText = ""
			for strTemp in strDBTextList:
				strDBText = strDBText + "<p>" + strTemp + "</p>"
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD_WIDTH(strText, 0, "title", "数据库用户", 20)
				if("error" in strDBText):
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)					
					nError  = nError + 1
				else:
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "content", "正常", 40)					
					nSuccess = nSuccess + 1
				strText = C_Mail_TR_End(strText)
			else:
				if("error" in strDBText):
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD_WIDTH(strText, 0, "title", "数据库用户", 20)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)	
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
					strText = C_Mail_TR_End(strText)		
			strDBText = L_Oracle_ClientConnect_Info(objOracleDBInfo, objConfigSysInfo.m_nDBLinkCount)
			if(objConfigSysInfo.m_nErrSend == 0):
				strText = C_Mail_TR_Begin(strText)
				strText = C_Mail_TD_WIDTH(strText, 0, "title", "链路连接数(" + str(objConfigSysInfo.m_nDBLinkCount) + ")", 20)
				if("error" in strDBText):
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
				else:
					strText  = C_Mail_TD_WIDTH(strText, 0, "content", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "content", "正常", 40)
					nSuccess = nSuccess + 1
				strText = C_Mail_TR_End(strText)
			else:
				if("error" in strDBText):
					strText = C_Mail_TR_Begin(strText)
					strText = C_Mail_TD_WIDTH(strText, 0, "title", "链路连接数(" + str(objConfigSysInfo.m_nDBLinkCount) + ")", 20)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", strDBText, 40)
					strText = C_Mail_TD_WIDTH(strText, 0, "error", "异常", 40)
					nError  = nError + 1
					strText = C_Mail_TR_End(strText)		
			
			strText = C_Mail_Table_End(strText)
			strText = C_Mail_Body_End(strText)
			strText = C_Mail_Html_End(strText)
		
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
	except Exception,e:
		#print "[main error]",Exception,":",e
		print traceback.format_exc()