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
		self.m_strLogKey     = ""
		self.m_nTimeInterval = 0
		self.m_nCheckLine    = 1
		self.m_strPath       = ""

#日志配置列表信息		
class CLogList():
	def __init__(self):
		self.m_objLogList = []
		
	def AddItem(self, strLogName, strKey, nTimeInterval, nCheckLine, strPath):
		objConfigLogInfo = CConfigLogInfo()
		objConfigLogInfo.m_strLogName    = strLogName
		objConfigLogInfo.m_strLogKey     = strKey
		objConfigLogInfo.m_nTimeInterval = nTimeInterval
		objConfigLogInfo.m_nCheckLine    = nCheckLine
		objConfigLogInfo.m_strPath       = strPath
		self.m_objLogList.append(objConfigLogInfo)
		
	def GetListCount(self):
		return len(self.m_objLogList)
		
	def GetPrecessInfo(self, nindex):
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
		nTimeInterval = 0
		nCheckLine    = 1
		strLogPath    = ""
		strLogInfo = strTemp.split(',')
		if(len(strLogInfo) == 2):
			strKey        = strLogInfo[0].strip()
			nTimeInterval = int(strLogInfo[1].strip())
		elif(len(strLogInfo) == 3):
			strKey        = strLogInfo[0].strip()
			nTimeInterval = int(strLogInfo[1].strip())	
			nCheckLine    = int(strLogInfo[2].strip())	
		elif(len(strLogInfo) == 4):
			strKey        = strLogInfo[0].strip()
			nTimeInterval = int(strLogInfo[1].strip())	
			nCheckLine    = int(strLogInfo[2].strip())	
			strLogPath 	  = strLogInfo[3].strip()
		elif(len(strLogInfo) == 0):
			strKey        = strdata[1].strip()
		
		objLogList.AddItem(strdata[0].strip(), strKey, nTimeInterval, nCheckLine, strLogPath)
		
		line = f.readline()  
	f.close()
	
#系统文件配置信息
class CConfigSysInfo:
	def __init__(self):
		self.m_nCpu        = 0
		self.m_nFreeMemory = 0	

#读取日志配置文件
def L_ReadSysConf(strFileName, objSysInfo):
	f = open(strFileName)
	line = f.readline() 
	while line:
		strdata = line.split('=')
		strTemp  = strdata[0].strip()
		
		#print("strTemp=%s,value=%s" %(strTemp, strdata[1]))
		if(strTemp == "CPU"):
			objSysInfo.m_nCpu = int(strdata[1].strip())
		elif(strTemp == "FreeMemory"):
			objSysInfo.m_nFreeMemory = int(strdata[1].strip())
		line = f.readline()  
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