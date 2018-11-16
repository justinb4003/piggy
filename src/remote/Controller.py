import socket

SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 9050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def init():
	sock.bind(('', SOCKET_PORT))

def shutdown():
	# not really used yet...
	pass
	sock.close()

def listenForCommand():
	data, addr = sock.recvfrom(1024)
	print("msg received:", data)
	return data
	
	

