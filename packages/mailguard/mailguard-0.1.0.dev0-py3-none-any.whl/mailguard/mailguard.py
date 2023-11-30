#!/usr/bin/python3

import email
import re,sys
import argparse
from colorama import Fore, Back, Style

print(Fore.GREEN+"""
			              _ _   ___                     _ 
			  /\/\   __ _(_) | / _ \_   _  __ _ _ __ __| |
			 /    \ / _` | | |/ /_\/ | | |/ _` | '__/ _` |
			/ /\/\ \ (_| | | / /_\\| |_| | (_| | | | (_| |
			\/    \/\__,_|_|_\____/ \__,_|\__,_|_|  \__,_|
                                              
	    	 Made by Mayank Rajput ⊙ NonRootedInsaan ⊙                                     
   
This is a forensic tool designed to facilitate the analysis of email headers, streamlining the process of identifying attackers swiftly. 
	""")

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="enter the raw(original) email file",type=str)
args=parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

# Reading the file Need to take the file as command line arguments argparse
f = open(args.file)
msg = email.message_from_file(f)
f.close()

parser.print_help()
print(Style.RESET_ALL)
parser = email.parser.HeaderParser()
headers = parser.parsestr(msg.as_string())


mailguard={
	"message-id":"",
	"spf-record":False,
	"dkim-record":False,
	"dmarc-record":False,
	"spoofed":False,
	"ip-address":"",
	"sender-client":"",
	"spoofed-mail":"",
	"dt":"",
	"content-type":"",
	"subject":""
}

for h in headers.items():

	# Message ID
	if h[0].lower()=="message-id":
		mailguard["message-id"]=h[1]


	# Mail server sending the mail
	if h[0].lower()=="received":
		mailguard["sender-client"]=h[1]

	# Authentication detected by mail server
	if h[0].lower()=="authentication-results":

		if(re.search("spf=pass",h[1])):
			mailguard["spf-record"]=True;

		if(re.search("dkim=pass",h[1])):
			mailguard["dkim-record"]=True
	
		if(re.search("dmarc=pass",h[1])):
			mailguard["dmarc-record"]=True

		if(re.search("does not designate",h[1])):
			mailguard["spoofed"]=True
			
		if(re.search("(\d{1,3}\.){3}\d{1,3}", h[1])):
			ip=re.search("(\d{1,3}\.){3}\d{1,3}", h[1])
			mailguard["ip-address"]=str(ip.group())
			# print("IP Address: "+ip.group()+"\n")

	if h[0].lower()=="reply-to":
		mailguard["spoofed-mail"]=h[1]

	if h[0].lower()=="date":
		mailguard["dt"]=h[1]

	if h[0].lower()=="content-type":
		mailguard["content-type"]=h[1]

	if h[0].lower()=="subject":
		mailguard["subject"]=h[1]

print(Fore.BLUE+"\n=========================Results=========================\n"+Style.RESET_ALL)

print(Fore.GREEN+"[+] Message ID"+mailguard["message-id"])

if(mailguard["spf-record"]):
	print(Fore.GREEN+"[+] SPF Records: PASS")
else:
	print(Fore.RED+"[+] SPF Records: FAIL")

if(mailguard["dkim-record"]):
	print(Fore.GREEN+"[+] DKIM: PASS")
else:
	print(Fore.RED+"[+] DKIM: FAIL")

if(mailguard["dmarc-record"]):
	print(Fore.GREEN+"[+] DMARC: PASS")
else:
	print(Fore.RED+"[+] DMARC: FAIL")

if(mailguard["spoofed"] and (not mailguard["spf-record"]) and (not mailguard["dkim-record"]) and (not mailguard["dmarc-record"])):
	print(Fore.RED+"[+] Spoofed Email Received")
	print(Fore.RED+"[+] Mail: "+mailguard["spoofed-mail"])
	print(Fore.RED+"[+] IP-Address:  "+mailguard["ip-address"])
else:
	print(Fore.GREEN+"[+] Authentic Email Received")
	print(Fore.GREEN+"[+] IP-Address:  "+mailguard["ip-address"])

print(Fore.GREEN+"[+] Provider "+mailguard["sender-client"])
print(Fore.GREEN+"[+] Content-Type: "+mailguard["content-type"])
print(Fore.GREEN+"[+] Date and Time: "+mailguard["dt"])
print(Fore.GREEN+"[+] Subject: "+mailguard["subject"]+"\n\n")