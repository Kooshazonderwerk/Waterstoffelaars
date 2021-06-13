#pip install time
import json
import time
#pip install socket
import socket

class Obstacle:
	
	def __init__(self, id, name, x1, y1, z1, x2, y2, z2):

		self.id = id
		self.name = name
		self.x1 = x1
		self.y1 = y1
		self.z1 = z1
		self.x2 = x2
		self.y2 = y2
		self.z2 = z2


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