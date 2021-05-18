from Room import Room
from Network import Network

class Program:

	def __init__(self, url):
		self.rooms = []
		self.network = Network(url)

	def getRooms(self):
		return self.rooms

	def addRoom(self, room):
		self.rooms.append(Room(room['id'], room['length'], room['width'], room['height'], room['sensors']))

	def addRoomsFromNetwork(self):
		rooms = self.network.getRooms()
		self.rooms = []
		for room in rooms:
			self.addRoom(room)

	def createRoom(self, name, width, height, length):
		self.network.createRoom(name, width, height, length)

	def editSensor(self, id, name, x, y, z):
		self.network.editSensor(id, name, x, y, z)

	def addSensor(self, roomId, name, x, y, z):
		self.network.addSensor(roomId, name, x, y, z)