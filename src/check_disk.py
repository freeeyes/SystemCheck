#!/bin/env python
# -*- coding: utf-8 -*- 
import os, sys, string
import commands 

#add by freeeyes

#�鿴LinuxӲ�̿ռ�ʹ�����
def L_disk(nDiskFreeAlarm):
	free = commands.getstatusoutput('df -h|egrep -v "tmp|var|shm"')
	list = free[1].split('\n')

	strName = ""  
	strText = ""
	for disk in range(len(list)):
		if disk < 2:
			continue
		#print("disk=%d" %(disk))
		a = list[disk].split()
		
		strFreeDisk = ""
		sttRote     = ""
		if(len(a) == 1):
			#����ֻ�о���
			strName = a[0]
			continue
		else:
			if(len(a) == 5):
				strFreeDisk = a[2]
				sttRote     = a[3]
				#print("1 (%d)strFreeDisk=%s,sttRote=%s" %(disk, strFreeDisk, sttRote))	
			elif(len(a)==6):
				strName = a[0]
				strFreeDisk = a[3]
				sttRote     = a[4]
				#print("2 (%d)strFreeDisk=%s,sttRote=%s" %(disk, strFreeDisk, sttRote))	
		
		#Ӳ�̿�ʹ�ÿռ��С
		nfreeDisk = 0
		if strFreeDisk[-1] == 'T':
			nfreeDisk = int(float(strFreeDisk[:-1]))*1024*1024
		elif strFreeDisk[-1] == 'G':
			nfreeDisk = int(float(strFreeDisk[:-1]))*1024
		else:
			nfreeDisk = int(float(strFreeDisk[:-1]))
		
		#Ӳ��ʹ����
		nFreeRote = 100 - int(sttRote[:-1])
		
		#��ʾ��Ϣ����
		if(nFreeRote <= nDiskFreeAlarm):
			strText = strText + "<p>volName(" + strName + "), Free(" + str(nfreeDisk) + " MB), FreeRote(" + str(nFreeRote) + "%)</p>"
	return strText
		
#���Դ���		
#if __name__ == "__main__": 
	 #L_disk()
	 #L_SendMail()