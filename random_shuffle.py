import datetime
import time
import struct 
import socket
from random import randint




def shuffle(filename, num):
	pkts = open(filename,'r')
	
	bname = filename[:filename.index('.')]
	outfiles = [open('tmp/' + bname + '_%d.sum' % i, 'w') for i in range(num)]
	base_stmp = 0
	interval = 60 # s

	for index, line in enumerate(pkts):
		if index % 10000 == 0:
			print index
		items = line.strip().split('|')
		# print items

		sip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(items[1])))[0]) 

		id = hash(str(sip)) % num
		
		# print temp, num, len(outfiles), index

		outfiles[randint(0,num-1)].write(line)	

	return
	

if __name__ == '__main__':
	shuffle('200101011400.sum', 100)