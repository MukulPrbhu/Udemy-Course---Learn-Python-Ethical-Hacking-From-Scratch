#!/usr/bin/env python

from platform import mac_ver
import string
import subprocess
import optparse

# This function helps in giving input to the File
# Like how commands have flags, specifying -i enables to enter Interface
# The if conditions are present to check if the flags are properly used
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Use this to add Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Specify an Interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options

# This is the main logic behind changing mac_ver
# There are 2 ways to use subprocess, one is to directly input a string
# but that will enable users to send in other commands, thus this method is used 
def change_mac(interface, new_mac):
    print("[-] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"]) 

# This function executes the ifconfig command and uses Regex to display the mac
# try https://pythex.org/ to practice regex
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_serach_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_serach_result:
        return mac_address_serach_result.group(0)
    else: 
        print("[-] Could not read MAC address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")