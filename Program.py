from Room import Room
from Network import Network
from SocketClient import SocketClient

class Program:

	def __init__(self, gui, url):
		self.gui = gui
		self.rooms = []
		self.network = Network(url)
		self.roomCount = 0
		self.webSockets = []
		self.addRoomsFromNetwork()
		for x in range(self.roomCount):
			self.webSockets.append(SocketClient(url, self, 1))

	def getRooms(self):
		return self.rooms

	def addRoom(self, room):
		self.rooms.append(Room(room['id'], room['name'], room['length'], room['width'], room['height'], room['sensors'], room['obstacles']))

	def addRoomsFromNetwork(self):
		rooms = self.network.getRooms()
		self.rooms = []
		self.roomCount = 0
		for room in rooms:
			self.roomCount += 1
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

	def updateSensorData(self, roomId, sensorValues):
		self.gui.updateSensorData(roomId, sensorValues)
	
	def startThreads(self):
		for t in self.webSockets:
			t.start()
	def stopThreads(self):
		for t in self.webSockets:
			t.stopThread()
			t.join()