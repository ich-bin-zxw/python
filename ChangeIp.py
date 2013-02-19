# authored by zhangxiaowei @2013.2.7
# for changing ip in OA,internet and test net

import wmi

ip=[["10.32.24.133"],["192.168.0.167"],["10.64.24.200"]]
netmask=[["255.255.255.0"],["255.255.255.0"],["255.255.255.0"]]
gateway=[["10.32.24.1"],["192.168.0.1"],["10.64.24.1"]]
dns=[['61.128.128.68',],['61.128.128.68',],['61.128.128.68',]]

wmiService = wmi.WMI()

def show_ip(show_message=True):
	for interface in wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True):
		if interface.Caption.split(" ",1)[1] == "Realtek RTL8168D(P)/8111D(P) PCI-E Gigabit Ethernet NIC":
			break;
	if(show_message==True):
		print("current ip 			",interface.IPAddress[0])
		print("current netmask 		",interface.IPSubnet[0])
		print("current gateway 		",interface.DefaultIPGateway[0])
		print("current dns 			",interface.DNSServerSearchOrder[0])
		print("------------------------------------------------------")
	return interface

def change_ip(choice):
	interface = show_ip(show_message=False)
	try:
		ret=interface.EnableStatic(IPAddress = ip[choice-1], SubnetMask = netmask[choice-1])
		if(ret[0]!=0 and ret[0]!=1):
			print("set ip error")
			return False

		ret=interface.SetGateways(DefaultIPGateway = gateway[choice-1],GatewayCostMetric = [1])
		if(ret[0]!=0 and ret[0]!=1):
			print("set gateway error")
			return False

		ret=interface.SetDNSServerSearchOrder(DNSServerSearchOrder = dns[choice-1])
		if(ret[0]!=0 and ret[0]!=1):
			print("set dns error")
			return False
		
	except:
		pass
	return True

def choice():
	
	while(1):	
		print("\n1.OA\n2.internet\n3.test net\n4.current ip\n5.exit\n")
		try:
			choice = int(input("your choice:"))
			print("\n\n")
		except:
			continue

		if choice==4:
			show_ip()
			continue

		if choice==5:
			break
		else:
			if(change_ip(choice)):
				print("-----------------change success-----------------")
				show_ip()



if __name__ == '__main__':
	choice()
