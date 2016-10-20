# analyze.py
# aggregate flow with port and ip address, only select the ones with more than 100 packet.
# aggregate by time, like 1 second, 15*60 = 900, and plot the flow with packet size, # of flows
# per second (P,F,B) # of packets, IP flows and bytes


import datetime
import time
import struct 
import socket
from util import packet
import util

# normalized entropy: H(X) = H'(X)/ N 
# N is the number of different values

def ins_sip_packet(pkt_list, packet):
	flag = False
	for id, pkt in enumerate(pkt_list):
		if pkt.equal_sip(packet):
			pkt.ins()
			flag = True
			break
	if not flag:
		pkt_list.append(packet)

def ins_dip_packet(pkt_list, packet):
	flag = False
	for id, pkt in enumerate(pkt_list):
		if pkt.equal_dip(packet):
			pkt.ins()
			flag = True
			break

	if not flag:
		pkt_list.append(packet)

def ins_sport_packet(pkt_list, packet):
	flag = False
	for id, pkt in enumerate(pkt_list):
		if pkt.equal_sport(packet):
			pkt.ins()
			flag = True
			break
	if not flag:
		pkt_list.append(packet)

def ins_dport_packet(pkt_list, packet):
	flag = False
	for id, pkt in enumerate(pkt_list):
		if pkt.equal_dport(packet):
			pkt.ins()
			flag = True
			break

	if not flag:
		pkt_list.append(packet)


def ins_all_packet(pkt_list, packet):
	flag = False
	for id, pkt in enumerate(pkt_list):
		if pkt.equal(packet):
			pkt.ins()
			flag = True
			break
	if not flag:
		pkt_list.append(packet)
	

def main(filename):
	pkts = open(filename,'r')
	fname =filename.split('.')[0]

	all_packets_list = []

	sip_list = []
	sport_list = []
	dip_list = []
	dport_list = []
	
	base_stamp = 0
	time_interval = 10 # 10s

	all_entropy_list = []
	sip_entropy_list = []
	sport_entropy_list = []
	dip_entropy_list = []
	dport_entropy_list = []
	
	timeid = 0
	for index, line in enumerate(pkts):
		if index % 10000 == 0:
			print index
		items = line.strip().split('|')
		
		try:
			timeindex = items[0].index('.') # seperate the float part of the seconds and convert to the only float with precision 0.001()
		except:
			timeindex = len(items[0])

		timeArray = time.strptime(items[0][:timeindex], "%Y-%m-%d %H:%M:%S")
		timestamp = int(time.mktime(timeArray))
		if items[0][timeindex:]!='':
			timestamp += float(items[0][timeindex:])

		if base_stamp + time_interval < timestamp:
			if base_stamp != 0:
				all_entropy_list.append( util.entropy(all_packets_list) )
				sip_entropy_list.append( util.entropy(sip_list) / len(sip_list))
				sport_entropy_list.append( util.entropy(sport_list) / len(sport_list))
				dip_entropy_list.append( util.entropy(sport_list) / len(dip_list))	
				dport_entropy_list.append( util.entropy(dport_list) / len(dport_list))
				
				file = open(fname+'_%d_count.txt' % timeid, 'w')
				for pkt in all_packets_list:
					file.write(pkt.to_string())
					file.write('\n')
				file.close()
				timeid += 1
			# clear all				
			base_stamp = timestamp
			all_packets_list = []

			sip_list = []
			sport_list = []
			dip_list = []
			dport_list = []

		sip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(items[1])))[0])     #ip address to int
		sport = int(items[2])
		dip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(items[3])))[0])     #ip address to int
		dport = int(items[4])
		protocol = int(items[5])
		size = int(items[6])

		a = packet(timestamp, sip, sport, dip, dport, protocol, size)
		
		ins_all_packet(all_packets_list, a)
		ins_sip_packet(sip_list, a)
		ins_dip_packet(dip_list, a)
		ins_dport_packet(dport_list, a)
		ins_sport_packet(sport_list, a)

	hfile = open(fname+'entropy.txt','w')
	hfile.write('|'.join(str(f) for f in sip_entropy_list))
	hfile.write('\n')
	hfile.write('|'.join(str(f) for f in sport_entropy_list))
	hfile.write('\n')
	hfile.write('|'.join(str(f) for f in dip_entropy_list))
	hfile.write('\n')
	hfile.write('|'.join(str(f) for f in dport_entropy_list))
	hfile.write('\n')
	hfile.write('|'.join(str(f) for f in sip_entropy_list))
	hfile.write('\n')
	hfile.close()
	return


if __name__ == '__main__':	
	for i in range(29, 100):
		print i, "---------------------------------------"
		main('tmp/200101011400_%d.sum' % i)

