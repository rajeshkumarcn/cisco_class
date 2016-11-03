#!/usr/bin/env python

import xmltodict
import json
from device import Device
import sys
import getpass
import requests

def show_cdp_nei(sw,ip1):
# this function connects to first switch and calls another function to connect to second switch onwards
	getdata1 = sw.show('show cdp nei detail')
	swlist=[ip1]
	# defining swsuccess and swfail as global variables
	global swsuccess
	global swfail
	global masteriplist
	swsuccess = [ip1]
	swfail = []
	masteriplist=[ip1]
	show_intf_dict = xmltodict.parse(getdata1[1])
	#following code displays the neighbors of first switch
	data1 = show_intf_dict['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_detail_info']['ROW_cdp_neighbor_detail_info']
	j=len(data1)
	#initiate a list to store Mgmt ip addresses of neighbors
	iplist=[]
	print "*****************************************************************************************************************"
	print "Number of neighbors of First Switch: " , j
	print "CDP Neighbors of First Switch" , swlist
	print "==================================="
	i=0
	for key,value in data1[i].iteritems():
		if i == j:
			continue
		else:
			print "Device  : " + data1[i]['device_id']
			print "Mgmt IP : " + data1[i]['v4mgmtaddr']
			print "Platform: " + data1[i]['platform_id']
			print "Local If: " + data1[i]['intf_id']
			print "RemoteIF: " + data1[i]['port_id']
			print "================================"
			iplist.append(data1[i]['v4mgmtaddr'])
			#print iplist[i]
			i=i+1
	print "Neighbors of first switch: "
	print iplist
	masteriplist.append(iplist)
	
	m=0
	#following loop logins to each neighboars of the first switch and calls a function to display cdp neighbors of them
	while m < j :
		iplist2=show_cdp_nei2(iplist[m])
		swlist.append(iplist[m])
		masteriplist.append(iplist2)
		print "Current Switch List " , swlist
		k=len(iplist2)
		i=0
		while (i < k): 
			if swlist.count(iplist2[i]):
				i=i+1
				continue
			else:
				iplist3=show_cdp_nei2(iplist2[i])
		   		swlist.append(iplist2[i])
		   		print "Current Switch List " , swlist
		   		i=i+1
		   		masteriplist.append(iplist3)
   		
   		m=m+1
	#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"   	
   	#print "Master IP List ", masteriplist
   	#The below functioning is for extending to the program to 4th level 
   	#n=0
   	#l=len(iplist3)

   	#while (n < l):
   	#	if swlist.count(iplist3[n]):
   	#		n=n+1
   	#		continue
   	#	else:
   	#		iplist4=show_cdp_nei2(iplist3[n])
   	#		swlist.append(iplist3[n])
   	#		print "Current Switch List ", swlist
   	#		n=n+1
   	#print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
   	#print "CDP neighbors of the following devices displayed"
   	#print swlist
   	#print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
   	print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
   	print "CDP neighbors of the following devices displayed"
   	print swsuccess
   	print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
   	print "###############################################################################################"
   	print "Login failed for the following devices"
   	print swfail
   	print "###############################################################################################"
	return data1

def show_cdp_nei2(sw):
	#this function logins to the switch and display the CDP neighbor details
	try:
		switch2 = Device(ip=sw, username='admin', password='cisco123')
		switch2.open()
		getdata2 = switch2.show('show cdp nei detail')
		show_intf_dict2 = xmltodict.parse(getdata2[1])
		data2 = show_intf_dict2['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_detail_info']['ROW_cdp_neighbor_detail_info']
		print "*****************************************************************************************************************"
		print "CDP Neighbors of Next Switch: " + sw
		print "==================================="
		iplist5=[]
		j= len(data2)
		i=0
		for key,value in data2[i].iteritems():
			if i == j:
				continue
			else:
				print "Device  : " + data2[i]['device_id']
				print "Mgmt IP : " + data2[i]['v4mgmtaddr']
				print "Platform: " + data2[i]['platform_id']
				print "Local If: " + data2[i]['intf_id']
				print "RemoteIF: " + data2[i]['port_id']
				print "==================================="
				iplist5.append(data2[i]['v4mgmtaddr'])
				#print iplist5[i]
				i=i+1
		k=len(iplist5)
		print ("Number of neighbors of next switch: " , k)
		print "Neighbors of next switch: "
		print iplist5
		#The following command appends the successful list with the switch IP address
		swsuccess.append(sw)		
		return iplist5
	except:
		#The following code is used in case the function is not able to login to the switch.
		print ("Unable to login to :" ,  sw)
		#The following code appends the failure list with the ip address of the switch.
		swfail.append(sw)
		iplist6=[]
		return iplist6


def main():
	
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    ip = raw_input("Enter IP Address of first device: ")
    username = raw_input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    try:
    	switch = Device(ip=ip, username=username, password=password)
    	#switch = Device(ip=ip, username='admin', password='cisco123')
        switch.open()
    	intf = show_cdp_nei(switch,ip)
    except: 
    	print "Unable to login to the device"
    	pass

if __name__ == "__main__":
    main()

