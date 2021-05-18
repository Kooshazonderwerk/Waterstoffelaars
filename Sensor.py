#pip install time
import json
import time
#pip install socket
import socket

class Sensor:
	
	def __init__(self, id, name, x, y, z):
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
		self.x = x
		self.y = y
		self.z = z

	'''returns the current value stored in the sensor object'''
	def getValue(self):
		return self.value


	'''Takes a float and changes the current value of the sensor object'''
	def setValue(self, value):
		self.value = value

	'''returns a tuple with 3 ints containing the current stored location of the sensor object'''
	def getLocation(self):
		return (self.x, self.y, self.z)

	'''Takes 3 ints and changes the current stored location of the sensor object'''
	def setLocation(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	'''returns a string with the id stored in the Sensor object'''
	def getId(self):
		return self.id

	'''returns a string with the name stored in the Sensor object'''
	def getName(self):
		return self.name