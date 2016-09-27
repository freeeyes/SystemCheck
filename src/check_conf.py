#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
from check_process import *

#进程配置信息
class CConfigProcessInfo:
	def __init__(self):
		self.m_strProcessName = ""
		self.m_nProcessCount  = 0

#进程配置列表信息		
class CProcessList():
	def __init__(self):
		self.m_objProcessList = []
		
	def AddItem(self, strProcessName, nCount):
		objConfigProcessInfo = CConfigProcessInfo()
		objConfigProcessInfo.m_strProcessName = strProcessName
		objConfigProcessInfo.m_nProcessCount  = nCount
		self.m_objProcessList.append(objConfigProcessInfo)
		
	def GetListCount(self):
		return len(self.m_objProcessList)
		
	def GetPrecessInfo(self, nindex):
		if(nindex >= len(self.m_objProcessList)):
			return None
		else:
			return self.m_objProcessList[nindex]
			
#日志文件配置信息
class CConfigLogInfo:
	def __init__(self):
		self.m_strLogName    = ""
		self.m_strLogType    = 2   #1是自动加后缀的时间文件，2是不加时间后缀的类型
		self.m_strLogKey     = ""
		self.m_nTimeInterval = 0
		self.m_nCheckLine    = 1
		self.m_strPath       = ""

#日志配置列表信息		
class CLogList():
	def __init__(self):
		self.m_objLogList = []
		
	def AddItem(self, strLogName, nLogType, strKey, nTimeInterval, nCheckLine, strPath):
		objConfigLogInfo = CConfigLogInfo()
		objConfigLogInfo.m_strLogName    = strLogName
		objConfigLogInfo.m_strLogType    = nLogType
		objConfigLogInfo.m_strLogKey     = strKey
		objConfigLogInfo.m_nTimeInterval = nTimeInterval
		objConfigLogInfo.m_nCheckLine    = nCheckLine
		objConfigLogInfo.m_strPath       = strPath
		self.m_objLogList.append(objConfigLogInfo)
		
	def GetListCount(self):
		return len(self.m_objLogList)
		
	def GetLogInfo(self, nindex):
		if(nindex >= len(self.m_objLogList)):
			return None
		else:
			return self.m_objLogList[nindex]		

#读取进程文件
def L_ReadProcessConf(strFileName, objProcessList):
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		objProcessList.AddItem(strdata[0].strip(), int(strdata[1].strip()))
	
		line = f.readline()  
	f.close()
	
#读取日志配置文件
def L_ReadLogConf(strFileName, objLogList):
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		strTemp  = strdata[1].strip()
		strKey        = ""
		nLogType      = 2
		nTimeInterval = 0
		nCheckLine    = 1
		strLogPath    = ""
		strLogInfo = strTemp.split(',')
		if(len(strLogInfo) == 2):
			strKey        = strLogInfo[0].strip()
			nLogType      = int(strLogInfo[1].strip())		
		elif(len(strLogInfo) == 3):
			strKey        = strLogInfo[0].strip()
			nLogType      = int(strLogInfo[1].strip())
			nTimeInterval = int(strLogInfo[2].strip())
		elif(len(strLogInfo) == 4):
			strKey        = strLogInfo[0].strip()
			nLogType      = int(strLogInfo[1].strip())
			nTimeInterval = int(strLogInfo[2].strip())	
			nCheckLine    = int(strLogInfo[3].strip())	
		elif(len(strLogInfo) == 5):
			strKey        = strLogInfo[0].strip()
			nLogType      = int(strLogInfo[1].strip())
			nTimeInterval = int(strLogInfo[2].strip())	
			nCheckLine    = int(strLogInfo[3].strip())	
			strLogPath 	  = strLogInfo[4].strip()
		elif(len(strLogInfo) == 0):
			strKey        = strdata[1].strip()
		
		objLogList.AddItem(strdata[0].strip(), nLogType, strKey, nTimeInterval, nCheckLine, strLogPath)
		
		line = f.readline()  
	f.close()
	
#系统文件配置信息
class CConfigSysInfo:
	def __init__(self):
		self.m_strName        = ""
		self.m_nCpu           = 0
		self.m_nFreeMemory    = 0	
		self.m_nDiskFreeAlarm = 10
		self.m_nErrSend       = 0  #0为全部状态发送，1为只发送错的
		self.m_nCheckDB       = 0  #0为不检测DB,1为检测DB
		self.m_nOnlineRote    = 10
		self.m_nDBDiskRote    = 10
		self.m_nDBLinkCount   = 500

#读取日志配置文件
def L_ReadSysConf(strFileName, objSysInfo):
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		strTemp  = strdata[0].strip()
		
		#print("[L_ReadSysConf]strTemp=%s,value=%s" %(strTemp, strdata[1]))
		if(strTemp == "CPU"):
			objSysInfo.m_nCpu = int(strdata[1].strip())
		elif(strTemp == "FreeMemory"):
			objSysInfo.m_nFreeMemory = int(strdata[1].strip())
		elif(strTemp == "NAME"):
			objSysInfo.m_strName = strdata[1].strip()
		elif(strTemp == "DiskFreeAlarm"):
			objSysInfo.m_nDiskFreeAlarm = int(strdata[1].strip())
		elif(strTemp == "SendError"):
			objSysInfo.m_nErrSend = int(strdata[1].strip())		
		elif(strTemp == "OnlineRote"):
			objSysInfo.m_nOnlineRote = int(strdata[1].strip())		
		elif(strTemp == "DBDiskRote"):
			objSysInfo.m_nDBDiskRote = int(strdata[1].strip())	
		elif(strTemp == "DBLinkCount"):
			objSysInfo.m_nDBLinkCount = int(strdata[1].strip())		
		elif(strTemp == "CheckDB"):
			objSysInfo.m_nCheckDB = int(strdata[1].strip())		
		line = f.readline()
		
#数据库配置文件
class CTestDBInfo:
	def __init__(self):
		self.m_strUserName = ""
		self.m_strPassword = ""

class COracleDBInfo:
	def __init__(self):
		self.m_strUserName   = ""
		self.m_strPassword   = ""
		self.m_strHostIP     = ""
		self.m_strPort       = ""
		self.m_strsid        = ""
		self.m_objTestDBInfo = []
		
#读取数据库配置文件
def L_ReadDBConf(strFileName, objDBInfo):
	nTestDBCount = 0
	strTestDBUser = ""
	strTestDBPass = ""
	
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		strTemp  = strdata[0].strip()

		#print("strTemp=%s,value=%s" %(strTemp, strdata[1]))
		if(strTemp == "USERNAME"):
			objDBInfo.m_strUserName = strdata[1].strip()
		elif(strTemp == "USERPASS"):
			objDBInfo.m_strPassword = strdata[1].strip()
		elif(strTemp == "HOSTIP"):
			objDBInfo.m_strHostIP   = strdata[1].strip()
		elif(strTemp == "PORT"):
			objDBInfo.m_strPort     = strdata[1].strip()	
		elif(strTemp == "SID"):
			objDBInfo.m_strsid      = strdata[1].strip()
		elif(strTemp == "TESTDBCOUNT"):
			#print "[L_ReadDBConf]TESTDBCOUNT=" + strTemp
			nTestDBCount      = int(strdata[1].strip())
		else:
			#寻找USER
			#print "[L_ReadDBConf]LEN=" + str(nTestDBCount)
			for i in range(1, nTestDBCount + 1):
				#print "[L_ReadDBConf]strTemp=" + strTemp
				if(strTemp  == "USER" + str(i)):
					strTestDBUser = strdata[1].strip()
					break
				if(strTemp  == "PASS" + str(i)):
					strTestDBPass = strdata[1].strip()
					objTestDBInfo = CTestDBInfo()
					objTestDBInfo.m_strUserName = strTestDBUser
					objTestDBInfo.m_strPassword = strTestDBPass
					strTestDBUser = ""
					strTestDBPass = ""
					print "[L_ReadDBConf]m_strUserName=" + objTestDBInfo.m_strUserName + ",strTestDBPass=" + objTestDBInfo.m_strPassword
					objDBInfo.m_objTestDBInfo.append(objTestDBInfo)
					break
			
		line = f.readline()
	
	print "[L_ReadDBConf]self.m_objTestDBInfo=" + str(len(objDBInfo.m_objTestDBInfo))
		
#邮件服务器配置信息
class CMailInfo:
	def __init__(self):
		self.m_strMailTo   = ""
		self.m_strMailFrom = ""
		self.m_strMailHost = ""
		self.m_nMailPort   = 0
		self.m_strUser     = ""
		self.m_strPass     = ""
		
def L_ReadMailConf(strFileName, objMailInfo):	
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		strTemp  = strdata[0].strip()
		
		#print("strTemp=%s,value=%s" %(strTemp, strdata[1]))
		if(strTemp == "MAILTO"):
			objMailInfo.m_strMailTo   = strdata[1].strip()
		elif(strTemp == "MAILFROM"):
			objMailInfo.m_strMailFrom = strdata[1].strip()
		elif(strTemp == "MAILHOST"):
			objMailInfo.m_strMailHost = strdata[1].strip()
		elif(strTemp == "PORT"):
			objMailInfo.m_nMailPort   = int(strdata[1].strip())	
		elif(strTemp == "USER"):
			objMailInfo.m_strUser     = strdata[1].strip()	
		elif(strTemp == "PASS"):
			objMailInfo.m_strPass     = strdata[1].strip()					
		line = f.readline()
		
#检测链接端口
#日志文件配置信息
class CConfigTCPInfo:
	def __init__(self):
		self.m_strIP    = ""
		self.m_strPort  = ""
		self.m_strName  = ""
		self.m_nType    = 0    #0为作为客户端，1位作为监听     

#日志配置列表信息		
class CTCPList():
	def __init__(self):
		self.m_objTcpList = []

	def AddItem(self, strIP, strPort, strName, nType):
		objConfigTCPInfo = CConfigTCPInfo()
		objConfigTCPInfo.m_strIP    = strIP
		objConfigTCPInfo.m_strPort  = strPort
		objConfigTCPInfo.m_strName  = strName
		objConfigTCPInfo.m_nType    = nType
		
		self.m_objTcpList.append(objConfigTCPInfo)
		
	def GetListCount(self):
		return len(self.m_objTcpList)
		
	def GetTcpInfo(self, nindex):
		if(nindex >= len(self.m_objTcpList)):
			return None
		else:
			return self.m_objTcpList[nindex]			

#读取TCP文件
def L_ReadTCPConf(strFileName, objTcpList):
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		strTemp = strdata[1].strip()
		strLogInfo = strTemp.split(',')
		objTcpList.AddItem(strdata[0].strip(), strLogInfo[0].strip(), strLogInfo[1].strip(), int(strLogInfo[2].strip()))
		line = f.readline()
		
	f.close()			
	
#检查消息队列
class CQueueInfo:
	def __init__(self):
		self.m_strQueueID  = ""
		self.m_nCount      = 500	
		
#队列配置列表信息		
class CQueueList():
	def __init__(self):
		self.m_objQueueList = []

	def AddItem(self, strQueueID, nCount):
		objQueueInfo = CQueueInfo()
		objQueueInfo.m_strQueueID = strQueueID
		objQueueInfo.m_nCount     = nCount
		self.m_objQueueList.append(objQueueInfo)
		
	def GetListCount(self):
		return len(self.m_objQueueList)
		
	def GetQueueInfo(self, nindex):
		if(nindex >= len(self.m_objQueueList)):
			return None
		else:
			return self.m_objQueueList[nindex]			
		
#读取消息队列文件
def L_ReadQueueConf(strFileName, objQueueList):
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		objQueueList.AddItem(strdata[0].strip(), int(strdata[1].strip()))
		line = f.readline()
	f.close()


'''	
#测试代码	
if __name__ == "__main__": 
	objProcessList = CProcessList()
	L_ReadFile("./process.conf", objProcessList)
	 
	for nindex in range(0, objProcessList.GetListCount()):
		objInfo = objProcessList.GetPrecessInfo(nindex)
		#print("(%d)m_strProcessName=%s,m_nProcessCount=%s" %(nindex, objInfo.m_strProcessName, objInfo.m_nProcessCount))
		objRet = L_Process(objInfo.m_strProcessName, objInfo.m_nProcessCount)
		if objRet == True:
			print("(%d)m_strProcessName=%s OK" %(nindex, objInfo.m_strProcessName))
'''		