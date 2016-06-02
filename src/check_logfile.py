#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import time
import datetime
import commands 

#add by freeeyes

#得到当前日志最后更新时间是否在指定时间内
def L_LogFile_State(strLogFileName, nTimeValue):
	ffiletime = os.stat(strLogFileName).st_mtime
	#print "1: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ffiletime)) 
	fNow = time.time()
	#print "2: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fNow)) 
	#print("[L_LogFile_State]timediff=%d" %(fNow - ffiletime))
	if(int(fNow - ffiletime) <= nTimeValue):
		return True
	else:
		return False
		
#获得按照每天日志的最后的信息是否包含关键词
def L_LogFile_Daily(strPath, strLogFileName, strkey, nLogLine, nTimeInterval):
	today        = datetime.date.today()
	strCurrYear  = str(today.year)
	
	strCurrMonth     = ""
	if(today.month < 10):
		strCurrMonth = "0" + str(today.month)
	else:
		strCurrMonth = str(today.month)
	
	strCurrDay       = ""
	if(today.day < 10):
		strCurrDay   = "0" + str(today.day)
	else:
		strCurrDay   = str(today.day)
	
	strLogFile = strPath + strLogFileName + "." + strCurrYear + strCurrMonth + strCurrDay
	#print("[L_LogFile_Daily]strLogFile=%s" %(strLogFile))
	
	#查看日志是否在指定时间内更新了
	if(nTimeInterval > 0):
		if(False == L_LogFile_State(strLogFile, nTimeInterval)):
			return 2
	
	strCommandLine = "tail -n 5 " + strLogFile
	#LineList = commands.getstatusoutput(strCommandLine)
	strLineList = os.popen(strCommandLine).read()
	LineList = strLineList.split('\n')
	for i in range(len(LineList)):
		#print("[L_LogFile_Daily](%d)disk=%s" %(i, LineList[i]))
		if(strkey in LineList[i]):
			return 0
	return 1

'''	
#测试代码
if __name__ == "__main__": 
	if(False == L_LogFile_State("./check_logfile.py", 600)):
		print("[L_LogFile_State]check_logfile.py time false")
		
	if(False == L_LogFile_Daily("/m2mjk/log/", "GetPlatID", "msisdn", 2)):
		print("[L_LogFile_Daily]False")
	else:
		print("[L_LogFile_Daily]True")
'''	