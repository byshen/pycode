"""
author: byshen
date: 10.5.2016

name: parse.py

purpose: 

parse the pcap file into several fields, parse result is a text file for later use
> source IP
> source port
> dest IP
> dest port
> time stamp
> ip header


> ethernet ARP, IP, IP6
> IP TCP,UDP,ICMP,ICMP6,SCTP
"""
import sys
import pcap
import dpkt
import util_print
import socket
import datetime
import time

def dump2sum(filepath):
    print filepath
    fname =filepath.split('.')[0]
    outfilepath = fname + '.sum'
    summaryfilepath = fname + '.summary'
    ptdict = {}

    infile = open(filepath)
    outfile = open(outfilepath, 'w')

    summaryfile = open(summaryfilepath, 'w')

    pcap = dpkt.pcap.Reader(infile)
                                    #main loop gathers necessary data from file
    counter = 0
    non_ip_counter = 0
    arp_counter = 0
    ip6_counter = 0

    start = time.time()
    for ts, buf in pcap:
       # # print buf
       #  if counter == 20001:
       #      break
        if counter % 10000 == 0:
            print "Packet No: ", counter 
        counter += 1
        try:
            packet_size = len(buf)
            # print packet_size

            eth = dpkt.ethernet.Ethernet(buf)       #ethernet layer 
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                if eth.type == dpkt.ethernet.ETH_TYPE_ARP:
                    arp_counter += 1
                elif eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ip6_counter += 1

                non_ip_counter += 1
                continue
            
            # all are IP now
            ip = eth.data                   #ip layer
            # print ip
            tcp = ip.data                   #tcp layer
            # print tcp
            protocol = ip.p

            #print ip
            srcaddr = socket.inet_ntoa(ip.src)      #plaintext representation of source ip address
            dstaddr = socket.inet_ntoa(ip.dst)      # dest. ip address
            sport = tcp.sport
            dport = tcp.dport



        #     # #print ip
        #     # print srcaddr`
        #     outfile.write('|'.join([str(datetime.datetime.utcfromtimestamp(ts)), \
        #         srcaddr,\
        #         str(sport),\
        #         dstaddr, \
        #         str(dport), \
        #         str(packet_size), \
        #         str(protocol)]))
        #     outfile.write('\n')

        #     # print str(protocol)
        #     if str(protocol) in ptdict:
        #         # print 'fuck here'
        #         ptdict[str(protocol)] += 1
        #     else:
        #         # print 'fuck there'
        #         ptdict[str(protocol)] = 1
        #     # print ptdict.keys()
        # except:                         #if we get here, the packet is not tcp/ip and should be ignored
        #     continue

    summaryfile.write('\n'.join( \
        [ 'total: '+ str(counter),\
          'non ip: ' + str(non_ip_counter),\
          'arp: ' + str(arp_counter),\
          'ip6: ' + str(ip6_counter),\
          str(ptdict)
        ]))

    infile.close()
    outfile.close()
    end = time.time()

    print end-start, "s elapsed."

if __name__ == '__main__':
    for i in range(1,32):
        if i in [1, 5]:
            continue
        text = "200101%02d1400.dump" % i
        dump2sum(text)

