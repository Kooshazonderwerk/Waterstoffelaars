from Room import Room
from Network import Network
from SocketClient import SocketClient
from SocketClientHandler import *

class Program:
	def __init__(self, gui, url):
		self.gui = gui
		self.rooms = {}
		self.network = Network(url)
		self.roomCount = 0
		# self.webSockets = []
		# self.addRoomsFromNetwork()
		self.socketconn = SocketClientHandler(self)
		print('my sid is', self.socketconn.sio.sid)
		# for key in self.rooms:
		# 	self.webSockets.append(SocketClient(url, self, self.rooms[key], self.socketconn))

	def getRooms(self):
		return self.rooms

	def addRoom(self, room):
		if room['id'] in self.rooms:
			self.rooms[room['id']].update(room)
		else:
			self.rooms[room['id']] = Room(room['id'], room['name'], room['length'], room['width'], room['height'], room['sensors'], room['obstacles'])

	def addRooms(self, rooms):
		for room in rooms:
			self.addRoom(room)
	
	def updateRooms(self, rooms):
		self.addRooms(rooms)
		self.gui.updateRooms()

	def addRoomsFromNetwork(self):
		rooms = self.network.getRooms()
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

	def updateSensorValue(self, roomId, sensorValues):
		self.gui.updateSensorValue(roomId, sensorValues)
	
	# def startThreads(self):
	# 	for t in self.webSockets:
	# 		t.start()
	
	def updateRoomData(self, roomId, roomInfo):
		newRoom = Room(roomInfo['id'], roomInfo['name'], roomInfo['length'], roomInfo['width'], roomInfo['height'], roomInfo['sensors'], roomInfo['obstacles'])
		self.rooms[roomId] = newRoom
		self.gui.updateRoomData(roomId, roomInfo)
	
	def getRoom(self, roomId):
		return self.rooms[roomId]