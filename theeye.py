#!/usr/bin/python3
# TheEye - Multi-threader - Integration Nmap + Slack

from pyfiglet import Figlet
from config import *
import subprocess
import threading
import argparse
import tempfile
import requests
import urllib3
import socket
import queue
import json
import os
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='Single host scan. E.g: -u http://hackerone.com', dest='url')
parser.add_argument('-U', '--urlslist', help='Mass host scan. E.g: -U file_name.txt', dest='urlslist')
parser.add_argument('-t', '--threads', help='You can change the threads. Default 5 E.g: -T 10', dest='threads', type=int, default=5)
parser.add_argument('-T', '--timeout', help='Define the timeout for Nmap. Default 20000 E.g: -T 20000', dest='time', type=int, default=20000)
args = parser.parse_args()

def main():
    print('           _ . - = - . _             ')
    print('       . "  \  \   /  /  " .         ')
    print('     ,  \                 /  .       ')
    print('   . \   _,.--~=~"~=~--.._   / .     ')
    print('  ;  _.-"  / \ !   ! / \  "-._  .    ')
    print(' / ,"     / ,` .---. `, \     ". \   ')
    print('/."   `~  |   /:::::\   |  ~`   ".\  ')
    print('\`.  `~   |   \:::::/   | ~`  ~ ."/  ')
    print(' \ `.  `~ \ `, `~~~" ,` /   ~`." /   ')
    print('  .  "-._  \ / !   ! \ /  _.-"  .    ')
    print('   ./    "=~~.._  _..~~=`"    \.     ')
    print('     ,/         ""          \,       ')
    print(' LGB   . _/             \_ .         ')
    print('          " - ./. .\. - "            ')

    custom_fig = Figlet(font='graffiti')
    print(custom_fig.renderText('The Eye'))

    def start_scanning():
        while True:
            url_request = queue_positions.get()
            scan_host(url_request)
            queue_positions.task_done()

    def add_single_url():
        hostname_resolved = socket.gethostbyname(args.url)
        scan_host(hostname_resolved)

    def add_urls_list():
        if os.path.isfile(args.urlslist):
            with open(args.urlslist, 'r') as list_file:
                    try:
                        for line in list_file:
                            queue_positions.put(socket.gethostbyname(line.strip()))
                        queue_positions.join()
                    except Exception:
                        print('[-] Host offline - {host}'.format(host=line))
                        pass
        else:
            print('Invalid file E.g: python3 theeye.py -U name_file_hosts.txt')
            exit()

    def scan_host(ip_target):
        try:
            print('Scanning: {ip_target}'.format(ip_target=ip_target))
            discovered_ports = subprocess.check_output('nmap -p- --min-rate={timeout} -T4 {ip} | grep ^[0-9] | cut -d "/" -f 1 | tr r"\n" ","'.format(ip=ip_target, timeout=args.time), shell=True).decode('utf-8').rstrip(',')
            
            if(len(discovered_ports) > 0):
                output_information = subprocess.check_output('nmap -A -p{ports} {ip}'.format(ports=discovered_ports, ip=ip_target), shell=True).decode('utf-8')
                try:
                    name_temp_file = save_host_information(output_information)
                    clean_host_information(name_temp_file.name)
                    prepare_send_notify(ip_target, name_temp_file.name, discovered_ports)
                    name_temp_file.close()
                except Exception as e:
                    print('[-] Error on send the information to Slack: {e}'.format(e=e))
            else:
                prepare_send_notify(ip_target, 'No ports found', discovered_ports)
        except Exception as e:
            print('[-] Error on scan the target'.format(e=e))
        
    def save_host_information(output_information):
        temp_file = tempfile.NamedTemporaryFile(mode = 'w+')
        temp_file.write(output_information)
        temp_file.seek(0)
        return temp_file

    def clean_host_information(temp_file_name):
        subprocess.call(["sed", "-i", "/NSE:/d;/NEXT SERVICE/d;/NSE Timing:/d;/Completed/d;/Starting/d;/Initiating/d;/Service detection/d;/Scanning/d;/Discovered/d;/SF/d;/unrecognized despite/d;/Nmap done/d;/Read data files/d;/Host is/d;/Scanned at/d;/NEXT SERVICE/d;/NSE Timing:/d",temp_file_name])

    def prepare_send_notify(ip_target, temp_file_name, discovered_ports):
        if len(temp_file_name) > 15:
            host_information = open(temp_file_name, 'r')
            file_read = host_information.read()
            notify_slack(ip_target, file_read, discovered_ports)
        else:
            notify_slack(ip_target, temp_file_name, discovered_ports)

    def notify_slack(ip_target, output_information, discovered_ports):
        try:
            webhook = posting_webhook
            if len(output_information) > 15:
                slack_data = {'text': 'Ports {discovered_ports} open on: {ip_target} {output_information}'.format(discovered_ports=discovered_ports, ip_target=ip_target, output_information=output_information)}
            else:
                slack_data = {'text': '{output_information} on: {ip_target}'.format(discovered_ports=discovered_ports, ip_target=ip_target, output_information=output_information)}
                
            requests.post(webhook, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
        except Exception as e:
            print('[-] Error in send the information to Slack: {e}'.format(e=e)) 

    queue_positions = queue.Queue(args.threads * 2)

    for i in range(args.threads):
        t = threading.Thread(target=start_scanning)
        t.daemon = True
        t.start()

    if args.url:
        add_single_url()
    elif args.urlslist:
        add_urls_list()
    else:
        'python3 theeye.py -h'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit()