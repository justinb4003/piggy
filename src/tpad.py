#!/usr/bin/python3

import socket
import time

commandList = ['DRIVE H10PCT', 'DRIVE STOP', 'SOLENOID 1 ON']

SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 9050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for c in commandList:
	sock.sendto(c.encode('utf-8'), (SOCKET_IP, SOCKET_PORT))
	time.sleep(1.00)

sock.close()

