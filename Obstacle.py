#pip install time
import json
import time
#pip install socket
import socket

class Obstacle:
	
	def __init__(self, id, name, x1, y1, z1, x2, y2, z2):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.settimeout(1.0)
		message = 'random'.encode()
		# change to your server ip address
		addr = ("127.0.0.1", 12000)
		client_socket.sendto(message, addr)
		
		try:
			data, server = client_socket.recvfrom(1024)
			resp_dict = json.loads(data.decode())
			self.value = resp_dict['value']
		except socket.timeout:
			print('REQUEST TIMED OUT')
			self.value = 0.0
		

		self.id = id
		self.name = name
		self.x1 = x1
		self.y1 = y1
		self.z1 = z1
		self.x2 = x2
		self.y2 = y2
		self.z2 = z2        

	def getValue(self):
		return self.value

        
	'''returns a tuple with 3 ints containing the current stored location of the Obstacle object'''
	def getLocation(self):
		return (self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)

	'''Takes 3 ints and changes the current stored location of the Obstacle object'''
	def setLocation(self, x1, y1, z1, x2, y2, z2):
		self.x1 = x1
		self.y1 = y1
		self.z1 = z1
		self.x2 = x2
		self.y2 = y2
		self.z2 = z2

	'''returns a string with the id stored in the Obstacle object'''
	def getId(self):
		return self.id

	'''returns a string with the name stored in the Obstacle object'''
	def getName(self):
		return self.name