from Room import Room
from Network import Network

class Program:

	def __init__(self, url):
		self.rooms = []
		self.network = Network(url)

	def getRooms(self):
		return self.rooms

	def addRoom(self, room):
		self.rooms.append(Room(room['id'], room['name'], room['length'], room['width'], room['height'], room['sensors'], room['obstacles']))

	def addRoomsFromNetwork(self):
		rooms = self.network.getRooms()
		self.rooms = []
		for room in rooms:
			self.addRoom(room)

	def createRoom(self, name, width, height, length):
		self.network.createRoom(name, width, height, length)
	
	def editRoom(self, id, name, width, height, length):
		self.network.editRoom(id, name, width, height, length)

	def editSensor(self, id, name, x, y, z):
		self.network.editSensor(id, name, x, y, z)

	def addSensor(self, roomId, name, x, y, z):
		self.network.addSensor(roomId, name, x, y, z)

	def editObstacle(self, id, name, x1, y1, z1, x2, y2, z2):
		self.network.editObstacle(id, name, x1, y1, z1, x2, y2, z2)

	def addObstacle(self, roomId, name, x1, y1, z1, x2, y2, z2):
		self.network.addObstacle(roomId, name, x1, y1, z1, x2, y2, z2)